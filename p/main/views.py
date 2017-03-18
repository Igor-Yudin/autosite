from django.shortcuts import render, redirect, get_object_or_404
from .forms import SiteParametersForm, ContentForm, FeaturesForm
from .models import SiteParameters, Content, Features
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.templatetags.staticfiles import static
# I change static for background and logo because decide that this properties will be set in css, but I didn't change fl-bl-image and single
# because they probably should set in html by content
# Подробное описание будующей системы смотри в файле Nostroweb дальнейшее развитие диплома
# В упрощенной версии диплома предлагается ввести параметры целевой аудитории, ключевые слова и
# контент: название, слоган, описание товара / услуги, о нас, контакты. Затемы автоматически
# создается сайт. Автоматическое создание подразумевает размещение указанного тектса по
# жестко заданному шаблону с добавлением изображений, фона и подбора шрифтов. Оучение проводится по цветам фона, темам изображений, размеру и цвету шрифта.

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

def choose_features(request, params_pk, content_pk):

	# 1. Произвести машинное обучение и выявить основные цвета: фона, текста. Размер и стиль
	# текста.
	# 2. По ключевым словам определить тему изображений, найти несколько фотографий для фона
	# и обычных картинок, при этом их цвет должен соответствовать выбранным, иначе заменить его цветом
	# 3. На этом контент заканчивается, передается дальше.
	# features:
	# font-family
	# header-size
	# p-size
	# main-background
	# main-headercolor
	# main-headersize
	# main-slogancolor
	# main-slogansize
	# about-us-background
	# about-us-headercolor
	# about-us-pcolor
	# about-good-background
	# about-good-headercolor
	# about-good-pcolor
	# contacts-background
	# contacts-headercolor
	# contacts-pcolor
	import requests
	url = 'https://1d931b481ffaebd16485:0cfcc2c5ae4283efe13ed2ec75d03d1611166071@api.shutterstock.com/v2/images/search'

	content = get_object_or_404(Content, pk = content_pk)
	params = {
		'url': url,
		'keys': content.keywords,
		'type': 'photo',
		'orientation': 'horizontal',
		'sort': 'popular',
	}

	r = requests.get('{url}?query={keys}&orientation={orientation}&image_type={type}&sort={sort}'.format(**params))

	image_url = None
	if r.status_code == 200 and r.json().get('total_count'):
		image_url = r.json()['data'][0]['assets']['preview']['url']
	else:
		print('Error: status code is {code}'.format(code = r.status_code))

	form = FeaturesForm(request.POST or None)
	if form.is_valid():
		features = form.save(commit = False)
		if image_url:
			features.main_background = image_url
		features.save()
		return redirect('show_page', params_pk = params_pk,
			content_pk = content_pk, features_pk = features.pk)
	else:
		return render(request, 'main/choose_features.html', {'form': form})
	# if request.method == "POST":
	# 	form = FeaturesForm(request.POST)
	# 	if form.is_valid():
	# 		features = form.save()
	# 		return redirect('show_page', params_pk = params_pk,
	# 			content_pk = content_pk, features_pk = features.pk)
	# else:
	# 	form = FeaturesForm()
	# return render(request, 'main/choose_features.html', {'form': form})

def show_page(request, params_pk, content_pk, features_pk):

	features = get_object_or_404(Features, pk = features_pk)
	content = get_object_or_404(Content, pk = content_pk)

	styles = create_styles(content, features)
	styles = create_css(styles)

	import os
	base_dir = os.path.dirname(os.path.abspath(__file__))
	
	with open("{0}/static/css/dynamic.css".format(base_dir), 'w') as file_obj:
		file_obj.write(styles)

	return render(request, 'main/success.html',
		{
			'content': content,
			'css': 'css/dynamic.css'
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

		'h1': {
			'font-size': features.header_size,
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
			'margin': '0 auto',
		},

		'.about_us_inf_block': {
			'margin': '0 auto',
		},

		'.contacts_inf_block': {
			'margin': '0 auto',
		},
	}

	for page in ['about_us', 'about_good', 'contacts']:
		if getattr(content, page, None):
			styles.update(turn_features_into_css_rules(page, features))
	else:
		styles.update(turn_features_into_css_rules('main', features))

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

	background = getattr(features, '%s_background' % page)
	header_color = getattr(features, '%s_header_color' % page)
	p_color = getattr(features, '%s_p_color' % page)

	styles = {
		class_name: {
			'background': (lambda b: 'url(%s)' % b if '.' in b
							else b)(background),
			'background-repeat': 'no-repeat',
			'background-size': 'cover',
			'background-position': 'center center',
			'background-attachment': 'scroll',
			# 'min-height': '20vh' if page == 'contacts' else '40vh',
		},

		header_class: {
			'color': header_color,
		},

		text_class: {
			'color': p_color,
		},
	}

	# Only main page has its sizes for header and slogan/p
	header_size = getattr(features, '%s_header_size' % page, None)
	p_size = getattr(features, '%s_p_size' % page, None)

	if header_size:
		styles[header_class].update({
			'font-size': header_size,
		})

	if p_size:
		styles[text_class].update({
			'font-size': p_size,
		})

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