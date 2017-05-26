from django.shortcuts import render, redirect, get_object_or_404
from .forms import SiteParametersForm, ContentForm, FeaturesForm
from .models import SiteParameters, Content, Features
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.templatetags.staticfiles import static
import pandas as pd
from sklearn.externals import joblib
from colorsys import rgb_to_hls, hls_to_rgb
import os
from enum import IntEnum
# I change static for background and logo because decide that this properties will be set in css, but I didn't change fl-bl-image and single
# because they probably should set in html by content
# Подробное описание будующей системы смотри в файле Nostroweb дальнейшее развитие диплома
# В упрощенной версии диплома предлагается ввести параметры целевой аудитории, ключевые слова и
# контент: название, слоган, описание товара / услуги, о нас, контакты. Затемы автоматически
# создается сайт. Автоматическое создание подразумевает размещение указанного тектса по
# жестко заданному шаблону с добавлением изображений, фона и подбора шрифтов. Оучение проводится по цветам фона, темам изображений, размеру и цвету шрифта.

# Const
NONE = 0
IMAGE = 1
COLOR = 2
COLORIMAGE = 3
SEPHEADER = 4

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class PageTypes(IntEnum):
	Image = 1
	Color = 2
	ColorImage = 3
	SepHeader = 4

# Create your views here.
def new_page(request):
	if request.method == "POST":
		form = SiteParametersForm(request.POST)
		if form.is_valid():
			site_params = form.save()
			return redirect('input_content', pk = site_params.pk)
	else:
		form = SiteParametersForm()
	return render(request, 'main/new_page.html', {'form': form})

def input_content(request, pk):
	"""
	Shows a fixed-structure form for content input.
	"""
	form = ContentForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		content = form.save()
		return redirect('choose_features', params_pk = pk, content_pk = content.pk)
	else:
		return render(request, 'main/input_content.html', {'form': form, 'pk': pk})

def get_input_parameters(site_parameters):
	with open('{0}/static/data/keywords.txt'.format(BASE_DIR)) as file_obj:
		keywords = file_obj.read()

	keywords_table = pd.DataFrame()
	for keyword in keywords.lower().split(','):
		keywords_table[keyword] = (0,)
	for keyword in site_parameters.keywords.lower().split(', '):
		keywords_table[keyword] = (1,)

	keywords_table['gender'] = site_parameters.gender
	keywords_table['age'] = site_parameters.age

	return keywords_table

def get_page_type(page, input_parameters):
	clf = joblib.load('{0}/static/data/{1}_type_clf.pkl'.format(BASE_DIR, page))
	page_type = clf.predict(input_parameters)
	return page_type

def get_page_color(page, input_parameters):
	clf = joblib.load('{0}/static/data/{1}_color_clf.pkl'.format(BASE_DIR, page))
	h, l, s = clf.predict(input_parameters)[0]
	rgb = hls_to_rgb(h, l, s)
	rgb = map(lambda x: format(int(x), '02x'), rgb)
	return '#{rgb}'.format(rgb = ''.join(rgb))

def get_page_theme(page, input_parameters):
	clf = joblib.load('{0}/static/data/{1}_theme_clf.pkl'.format(BASE_DIR, page))
	page_theme = clf.predict(input_parameters)
	return ', '.join(page_theme)

def get_image_url(themes):
	import requests
	url = 'https://1d931b481ffaebd16485:0cfcc2c5ae4283efe13ed2ec75d03d1611166071@api.shutterstock.com/v2/images/search'

	params = {
		'url': url,
		'keys': themes,
		'type': 'photo',
		'orientation': 'horizontal',
		'sort': 'popular',
	}

	r = requests.get('{url}?query={keys}&orientation={orientation}&image_type={type}&sort={sort}'.format(**params))

	image_url = ''
	if r.status_code == 200 and r.json().get('total_count'):
		image_url = r.json()['data'][0]['assets']['preview']['url']
	else:
		print('Error: status code is {code}'.format(code = r.status_code))
	return image_url

def get_font_colors(page_type, page_background):
	"""
	Returns colors for header and paragraphs.
	Header color is figuring out for background
	and paragraph color is a little bit lighter.
	"""
	def get_background_color(background):
		from PIL import Image
		import requests
		from io import BytesIO

		if '.' in background:
			response = requests.get(background)
			image = Image.open(BytesIO(response.content))

			# Colors frequenties
			colors_freq = {}

			for pixel_color in image.getdata():
				if colors_freq.get(pixel_color):
					colors_freq[pixel_color] += 1
				else:
					colors_freq[pixel_color] = 1

			# Choose the most frequently color
			color = max(colors_freq, key = lambda color: colors_freq[color])

			# Skip alpha component
			color = color[:-1] if len(color) > 3 else color

			return '#' + ''.join(format(channel, '02x') for channel in color)
		else:
			return background

	def get_color_seperating_for(color):
		a_color = color[1:]
		a_color = list(map(''.join, zip(* [iter(a_color)] * 2)))
		a_color = list(map(lambda x: int(x, 16), a_color))
		
		colors = ((17, 17, 17), (119, 119, 119), (255, 255, 255))

		difs = []
		for b_color in colors:
			# Calculate distance for each color (sum of each channel difference squared)
			dif = sum(map(lambda a, b: (a - b) ** 2, a_color, b_color))
			difs.append(dif)
		ind = difs.index(max(difs))

		return '#' + ''.join(format(channel, '02x') for channel in colors[ind])

	def get_darker_color(color):
		color = color[1:]
		color = list(map(''.join, zip(* [iter(color)] * 2)))
		color = list(map(lambda x: int(x, 16), color))
		darker_color = list(map(lambda x: x + 20 if x + 20 <= 255 else 255, color))
		return '#' + ''.join(format(channel, '02x') for channel in darker_color)

	background_color = get_background_color(page_background)
	h_color = get_color_seperating_for(background_color)

	if page_type == SEPHEADER:
		p_color = '#161616'
	else:
		p_color = get_darker_color(h_color)
	return h_color, p_color

def choose_features(request, params_pk, content_pk):

	# 1. Произвести машинное обучение и выявить основные цвета: фона, текста. Размер и стиль
	# текста.
	# 2. По ключевым словам определить тему изображений, найти несколько фотографий для фона
	# и обычных картинок, при этом их цвет должен соответствовать выбранным, иначе заменить его цветом
	# 3. На этом контент заканчивается, передается дальше.

	site_params = get_object_or_404(SiteParameters, pk = params_pk)

	# Machine learning
	page_features = {}
	input_parameters = get_input_parameters(site_params)
	for page in ('main', 'about_good', 'about_us', 'contacts'):
		page_type = get_page_type(page, input_parameters)
		page_features['%s_type' % page] = page_type

		page_color = get_page_color(page, input_parameters)
		page_features['%s_color' % page] = page_color

		# page_theme = get_page_theme(page, input_parameters)
		# page_features['%s_theme' % page] = page_theme

		page_theme = site_params.keywords

		# Set page background image
		if page_type != COLOR and page_type != NONE and page_theme != 'none':
			page_image = get_image_url(page_theme)
			page_features['%s_image' % page] = page_image
			if not page_image:
				page_features['%s_type' % page] = COLOR

		h_color, p_color = get_font_colors(page_type, page_image) # '#161616', '#333333'
		page_features['%s_h_color' % page] = h_color
		page_features['%s_p_color' % page] = p_color

		if page == 'main':
			page_features['%s_h_size' % page] = 120
			page_features['%s_p_size' % page] = 48

	features = Features()
	features.font_family = 'Arial'
	features.h_size = 48
	features.p_size = 20

	for k, v in page_features.items():
		setattr(features, k, v)
	features.save()
	return redirect('show_page', params_pk = params_pk,
								 content_pk = content_pk,
								 features_pk = features.pk)

def show_page(request, params_pk, content_pk, features_pk):

	features = get_object_or_404(Features, pk = features_pk)
	content = get_object_or_404(Content, pk = content_pk)

	styles = create_styles(content, features)
	styles = create_css(styles)

	with open("{0}/static/css/dynamic.css".format(BASE_DIR), 'w') as file_obj:
		file_obj.write(styles)

	return render(request, 'main/success.html',
		{
			'content': content,
			'css': 'css/dynamic.css',
			'types': PageTypes,
			'pages': ('about_good', 'about_us', 'contacts'),
			'features': features,
		})

def create_styles(content, features):
	"""
	Returns dictonary which is repersentation of css rules.

	"""
	styles = {
		# Set common styles
		'*': {
			'margin': '0px',
			'padding': '0px',
			'border': '0px',
			'font-size': '100%',
			'font': 'inherit',
			'vertical-align': 'baseline',
			'box-sizing': 'border-box',
		},


		# Set font

		'body': {
			'line-height': '1',
			'font-family': features.font_family,
		},

		'h1, h2': {
			'font-size': features.h_size,
			'text-align': 'center',
		},

		'p': {
			'font-size': features.p_size,
			'text-align': 'center',
		},

		# Set sizes, position, margin

		'html, body': {
			'width': '100%',
			'height': '100%',
		},

		'section': {
			'position': 'relative',
			'min-height': '20vh',
			'height': 'auto',
			'overflow': 'hidden',
		},

		'.inf_block_wrapper': {
			# 'position': 'absolute',
			# 'margin': 'auto',
			# 'left': '0',
			# 'right': '0',
			# 'top': '0',
			# 'bottom': '0',
			# 'display': 'inline-table',
			# 'width': '75%',
			'width': '75%',
		},

		'.main_inf_block': {
			'margin': '25vh auto 35vh auto',
		},

		'.logo': {
			'position': 'absolute',
			'top': '0',
			'left': '0',
			'width': '200px',
		},

		'.logo img': {
			'width': '100%',
			'height': 'auto',
		},

		'.about_good_inf_block': {
			'margin': '15vh auto 35vh auto',
		},

		'.about_us_inf_block': {
			'margin': '15vh auto 35vh auto',
		},

		'.contacts_inf_block': {
			'margin': '15vh auto 35vh auto',
		},

		'.sepheader': {
			'padding': '150px',
		},

		'.subheader': {
			'background': '#ffffff',
		},

		'.inf_block_wrapper h2': {
			'margin-bottom': '15vh',
		},

		'img': {
			'margin-left': 'calc(100% / 5)',
			'width': '60%',
			'margin-top': '5vh',
			'border-radius': '70px',
		},
	}

	# Здесь есть функция, которая делает (if getattr), которая
	# позволяет выставлять свойства только для выбранных страниц, я временно эту возможность убираю

	for page in ('main', 'about_good', 'about_us', 'contacts'):
		# if getattr(content, page, None):
		styles.update(turn_features_into_css_rules(page, features))
	# else:
	# 	styles.update(turn_features_into_css_rules('main', features))

	return styles

def turn_features_into_css_rules(page, features):
	"""
	This method creates a dictionary that is the css-rules
	representation of features for page.
	Get page name and features-object, containing fields
	for all pages.

	Returns dict of css rules for the page.

	"""

	assert page is not "", "Page is an empty string"
	assert page in ["main", "about_us", "about_good", "contacts"], 'Page name is incorrect'
	assert isinstance(features, Features), "features is not an instance of Features"

	class_name = '.' + page
	header_class = class_name + ' h1' 
	text_class = class_name + ' p'

	page_type = getattr(features, '%s_type' % page)
	color = getattr(features, '%s_color' % page)
	image = getattr(features, '%s_image' % page)
	h_color = getattr(features, '%s_h_color' % page)
	p_color = getattr(features, '%s_p_color' % page)

	styles = {
		class_name: {
			'background': 'url(%s)' % image if page_type == IMAGE else color,
			'background-repeat': 'no-repeat',
			'background-size': 'cover',
			'background-position': 'center center',
			'background-attachment': 'scroll',
			# 'min-height': '20vh' if page == 'contacts' else '40vh',
		},

		header_class: {
			'color': h_color,
		},

		text_class: {
			'color': p_color,
		},
	}

	# Only main page has its sizes for header and slogan/p
	h_size = getattr(features, '%s_h_size' % page, None)
	p_size = getattr(features, '%s_p_size' % page, None)

	if h_size:
		styles[header_class].update({
			'font-size': h_size,
		})

	if p_size:
		styles[text_class].update({
			'font-size': p_size,
		})

	# set specific styles for sepheader
	if page_type == SEPHEADER:
		sepheader_class = class_name + ' .sepheader'
		styles.update({
			sepheader_class: {
				'background': 'url(%s)' % image,
				'background-repeat': 'no-repeat',
				'background-size': 'cover',
				'background-position': 'center center',
				'background-attachment': 'scroll',
				}
			})
		styles[class_name]['background'] = '#ffffff'

	return styles

def create_css(styles):
	"""
	It returns a string that represents a css file
	THAT SHOULD BE OPTIMISED, CAUSE THIS CONCONTENTATE IMMUTABLE STR, THAT IS VERY SLOWLY
	"""
	css = ""
	for elem, style in sorted(styles.items()):
		css += elem + ' {\n'
		# CSS rules should be sorted,
		# it proves background goes first before other
		# rules about background and won't lead to overriding, probably should use oredered dictionary instead
		for feature, value in sorted(styles[elem].items()):
			css += '\t{0}: {1};\n'.format(feature, value)
		css += '}\n\n'
	return css