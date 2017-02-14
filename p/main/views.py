from django.shortcuts import render, redirect, get_object_or_404
from .forms import SiteParametersForm, ContentForm, FeaturesForm
from .models import SiteParameters, Content, Features, Image
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.templatetags.staticfiles import static
import json
# I change static for background and logo because decide that this properties will be set in css, but I didn't change fl-bl-image and single
# because they probably should set in html by content

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
	Gets request, pk - key for input parameters in database from previous form
	This view returns a form for content input and turn data from this form into json-string,
	save it in database and redirects to choose features form.
	POST STRUCTURE

	# List of pages
	-pages

	# Main page properties
	-main-background
	-logo
	-name
	-slogan

	# Usual page properties
	-page-background
	-page-single
	-page-header
	-page-p-count
	[
	-page-p-i-image
	-page-p-i-background
	-page-p-i-text
	-page-p-i-header
	]
	"""
	if request.method == "POST":
		content = dict()
		pages = request.POST.get('pages')
		content['order'] = pages
		for page in pages.split(','):
			if page == 'main':

				background_url = "" # Use background_url to safe from unknown variables in lambda
				if request.FILES.get('%s-background' % page):
					background = Image.objects.create(image = request.FILES.get('%s-background' % page))
					background_url = background.image.url

				logo_url = ""
				if request.FILES.get('logo'):
					logo = Image.objects.create(image = request.FILES.get('logo'))
					logo_url = logo.image.url

				content.update(
					{
						page: {
							'logo': (lambda url: url if url else None)(logo_url),
							'header': request.POST.get('name'),
							'slogan': request.POST.get('slogan'),
							'background': (lambda url: url if url else None)(background_url),
						}
					}
				)
			else:
				background_url = ""
				if request.FILES.get('%s-background' % page):
					background = Image.objects.create(image = request.FILES.get('%s-background' % page))
					background_url = background.image.url

				single_url = ""
				if request.FILES.get('%s-single' % page):
					single = Image.objects.create(image = request.FILES.get('%s-single' % page))
					single_url = single.image.url

				content.update(
					{
						page: {
							'header': request.POST.get('%s-header' % page),
							'single-image': (lambda url: url if url else None)(single_url),
							'background': (lambda url: url if url else None)(background_url),
						}
					}
				)
				paragraphs_count = int(request.POST.get('%s-p-count' % page))
				if paragraphs_count != 0:
					#Initialization
					p_images_url = ["" for i in range(paragraphs_count)]
					p_images = ["" for i in range(paragraphs_count)]
					p_backgrounds_url = ["" for i in range(paragraphs_count)]
					p_backgrounds = ["" for i in range(paragraphs_count)]

					# Fill in images and background
					for i in range(paragraphs_count):
						file = request.FILES.get('%s-p-%s-image' % (page, i + 1))
						if file:
							p_images[i] = Image.objects.create(image = file)
							p_images_url[i] = p_images[i].image.url

					for i in range(paragraphs_count):
						file = request.FILES.get('%s-p-%s-background' % (page, i + 1))
						if file:
							p_backgrounds[i] = Image.objects.create(image = file)
							p_backgrounds_url[i] = p_backgrounds[i].image.url

					# Update content dict with page paragraphs, consisting from header, text, image, background
					content[page]['paragraphs'] = [
						{
							'header': request.POST.get('%s-p-%s-header' % (page, i + 1)),
							'text': request.POST.get('%s-p-%s-text' % (page, i + 1)),
							'image': (lambda url: url if url else None)(p_images_url[i]),
							'background': (lambda url: url if url else None)(p_backgrounds_url[i]),
						}
						for i in range(paragraphs_count)
					]
		content = Content.objects.create(text = json.dumps(content))
		return redirect('choose_features', params_pk = pk, content_pk = content.pk)
	else:
		form = ContentForm()
	return render(request, 'main/input_content.html', {'form': form, 'pk': pk})

def choose_features(request, params_pk, content_pk):
	if request.method == "POST":
		form = FeaturesForm(request.POST)
		if form.is_valid():
			features = form.save()
			return redirect('show_page', params_pk = params_pk, content_pk = content_pk, features_pk = features.pk)
	else:
		form = FeaturesForm()
	return render(request, 'main/choose_features.html', {'form': form})

def show_page(request, params_pk, content_pk, features_pk):
	# with open(r'C:\Users\IO\bach\p\criteria.txt') as file_obj:
	# 	inf = file_obj.read()

	inf = get_object_or_404(Features, pk = features_pk)
	inf = inf.text

	inf = inf.translate({ord(char) : None for char in '\r'})
	inf = inf.split('\n\n')

	content = get_object_or_404(Content, pk = content_pk)
	content = content.to_dict()
	pages = content['order'].split(',')

	page_features = {}
	for page in inf:
		page = page.split('\n')
		page_features[page[0]] = page[1:]

	styles = {

		# Set common styles
		'*': {
			'margin': '0px',
			'padding': '0px',
		},

		'html, body': {
			'width': '100%',
			'height': '100%',
		},

		# Set helpful rules
		'.centered-top-30vh': {
			'padding-top': '30vh',
			'margin': '0 auto',
		},

		'.completely-centered': {
			'position': 'absolute',
			'margin': 'auto',
			'left': '0',
			'right': '0',
			'top': '0',
			'bottom': '0',
			# Very strange... but it works
			'display': 'inline-table',
		},
	}

	for page in pages:
		features = dict()
		for line in page_features[page]:
			line = line.split(': ')
			features[line[0]] = line[1]
			# For changing background and logo images
			for c in content[page].keys():
				if c == 'background' or c == 'logo': # or p == 'single'
					features[c] = content[page][c]
			#
		turn_features_into_css_rules(styles, features, page)

	import os
	base_dir = os.path.dirname(os.path.abspath(__file__))
	styles = create_css(styles)
	
	with open(str.format("{0}\static\css\dynamic.css", base_dir), 'w') as file_obj:
		file_obj.write(styles)

	return render(request, 'main/success.html', { 'pages': pages, 'content': content, 'raw': styles, 'css': 'css\dynamic.css' })

def turn_features_into_css_rules(common_styles, features, page_name):
	"""
	Add css rules to common_styles for class with name '.page_name'
	"""
	class_name = '.' + page_name
	styles = {
		# Set page properties: background, height
		class_name: {
			'position': 'relative',
			'background': (lambda background: 
								'url({0})'.format(background) if '.' in background
								else background)(features['background']),
			'background-repeat': 'no-repeat',
			'background-size': 'cover',
			'background-position': 'center center',
			'background-attachment': features['attachment'],
			'height': features['page-height'],
		},

		# Set inf-block on main page properties: width, font-family
		class_name + ' .inf-block': {
			'width': features['inf-block-width'],
			'font-family': features['font-family'],
		},

		# Set header on main page properties: color, size, align
		class_name + ' .inf-block h1': {
			'text-align': 'center',
			'color': features['main-text-color'],
			'font-size': features['main-text-size'],
		},

		#Set slogan on main page properties: color, size, align
		class_name + ' .inf-block p': {
			'text-align': 'center',
			'color': features['font-color'],
			'font-size': features['font-size'],
		},

		# Set empty rules
		class_name + ' .logo-position': {
		},

		class_name + ' .inf-block-position': {
		},
	}

	# Set effects on background: darken, blur or none
	if features.get('effects') == 'darken':
		styles[class_name]['background'] = 'linear-gradient(rgba(0, 0, 0, .7), \
		rgba(0, 0, 0, .7)), ' + styles[class_name]['background']
	elif features.get('effects') == 'none':
		pass
	elif features.get('effects') == 'blur':
		pass
	elif features.get('effects') == 'darken blur':
		pass

	# Set logo on page: image, size
	if features.get('logo'):
		styles.update(
			{
				class_name + ' .logo': {
				'background-image': str.format('url({0})',features['logo']),
				'background-repeat': 'no-repeat',
				'background-size': 'contain',
				'background-position': 'center center',
				'height': features['logo-height'],
				'width': features['logo-width'],
				}
			})

	# Set logo position on main page
	if features.get('logo-position') == 'top left':
		styles[class_name + ' .logo-position']['position'] = 'absolute'
		styles[class_name + ' .logo-position']['left'] = '0px'
		styles[class_name + ' .logo-position']['top'] = '0px'
	elif features.get('logo-position') == 'completely-centered':
		styles[class_name + ' .logo-position']['position'] = 'absolute'
		styles[class_name + ' .logo-position']['margin'] = 'auto'
		styles[class_name + ' .logo-position']['left'] = '0px'
		styles[class_name + ' .logo-position']['top'] = '0px'
		styles[class_name + ' .logo-position']['right'] = '0px'
		styles[class_name + ' .logo-position']['bottom'] = '0px'

	# Set inf-block position
	if features.get('inf-block-align') == 'center':
		styles[class_name + ' .inf-block-position']['position'] = 'absolute'
		styles[class_name + ' .inf-block-position']['margin'] = 'auto'
		styles[class_name + ' .inf-block-position']['left'] = '0'
		styles[class_name + ' .inf-block-position']['right'] = '0'
	elif features.get('inf-block-align') == 'left':
		styles[class_name + ' .inf-block-position']['position'] = 'absolute'
		styles[class_name + ' .inf-block-position']['margin'] = 'auto'
		styles[class_name + ' .inf-block-position']['left'] = '0'
	elif features.get('inf-block-align') == 'right':
		styles[class_name + ' .inf-block-position']['position'] = 'absolute'
		styles[class_name + ' .inf-block-position']['margin'] = 'auto'
		styles[class_name + ' .inf-block-position']['right'] = '0'

	# Set inf-block vertical position
	if features.get('inf-block-v-align') == 'center':
		styles[class_name + ' .inf-block-position']['top'] = '0'
		styles[class_name + ' .inf-block-position']['bottom'] = '0'
		styles[class_name + ' .inf-block-position']['display'] = 'inline-table'
	elif features.get('inf-block-v-align') == 'to-top':
		styles[class_name + ' .inf-block-position']['top'] = '15vh'
	elif features.get('inf-block-v-align') == 'to-bottom':
		styles[class_name + ' .inf-block-position']['bottom'] = '15vh'
	
	# Set float-block properties
	if features.get('columns') != 'none':
		columns_count = features.get('columns')
		styles.update(
			{
				class_name + ' .float-block':
				{
					'width': str(100 / int(columns_count) - 1) + '%',
					'display': 'inline-block',
					'background': (lambda background: 
								'url({0})'.format(static(background)) if '.' in background
								else background)(features['fl-block-background']),
				},
				class_name + ' .float-block .float-block-header h1':
				{
					'text-align': features['fl-bl-header-align'],
					'font-size': features['header-size'],
					'color': features['header-color'],
				},
				class_name + ' .float-block .float-block-text p':
				{
					'text-align': features['fl-bl-text-align'],
					'font-size': features['font-size'],
					'color': features['font-color'],
				},
				class_name + ' .float-block .float-block-image':
				{
					# Is set in html code, but probably should be there through content variables
					# 'background-image': "",
					#height and width should be set automatically
					'width': '100px',
					'height': '100px',
					'float': (lambda position:
										'none' if position == 'top'
										else position)
										(features.get('fl-image-position')),
					'background-size': 'contain',
					'margin': '0 auto', # center it
				},
			})
		if features.get('fl-image-form') == 'round':
			styles[class_name + ' .float-block .float-block-image']['border-radius'] = '50%'
		
		# Set single-image
		if features.get('fl-single-image') != 'none':
			styles.update(
				{
					class_name + ' .single-image':
					{
						'width': '100px',
						'hieght': '100px',
						'padding': '0 20px',
						'background-image': str.format('url({0})', static(features['fl-single-image'])),
					},
				})

	common_styles.update(styles)

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
			css += str.format('\t{0}: {1};\n', feature, value)
		css += '}\n\n'
	return css