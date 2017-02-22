from django.shortcuts import render, redirect, get_object_or_404
from .forms import SiteParametersForm, ContentForm, FeaturesForm
from .models import SiteParameters, Content, Features
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.templatetags.staticfiles import static
import json
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

	
	if request.method == "POST":
		form = FeaturesForm(request.POST)
		if form.is_valid():
			features = form.save()
			return redirect('show_page', params_pk = params_pk,
				content_pk = content_pk, features_pk = features.pk)
	else:
		form = FeaturesForm()
	return render(request, 'main/choose_features.html', {'form': form})

def show_page(request, params_pk, content_pk, features_pk):

	features = get_object_or_404(Features, pk = features_pk)
	content = get_object_or_404(Content, pk = content_pk)
	styles = create_styles(content, features)

	import os
	base_dir = os.path.dirname(os.path.abspath(__file__))
	styles = create_css(styles)
	
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
		},

		'html, body': {
			'width': '100%',
			'height': '100%',
		},

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

		'.inf-block-wrapper': {
			'position': 'absolute',
			'margin': 'auto',
			'left': '0',
			'right': '0',
			'width': '75%',
		},

		'.logo': {
			'position': 'absolute',
			'top': '0',
			'left': '0',
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
	Returns dict with css rules for the page.

	"""
	class_name = '.' + page.replace('_', '-')

	background = getattr(features, '%s_background' % page)
	header_color = getattr(features, '%s_header_color' % page)
	p_color = getattr(features, '%s_p_color' % page)

	# Only main page features
	header_size = getattr(features, '%s_header_size' % page, None)
	p_size = getattr(features, '%s_p_size' % page, None)

	styles = {
		class_name: {
			'background': (lambda b: 'url(%s)' % b if '.' in b
							else b)(background),
			'background-repeat': 'no-repeat',
			'background-size': 'cover',
			'background-position': 'center center',
			'background-attachment': 'scroll',
			'height': '100vh',
		},

		class_name + ' h1': {
			'color': header_color,
		},

		class_name + ' p': {
			'color': p_color,
		},
	}

	if header_size:
		styles[class_name + ' h1'].update({
			'font-size': header_size,
		})

	if p_size:
		styles[class_name + ' p'].update({
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