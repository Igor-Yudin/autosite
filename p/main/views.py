from django.shortcuts import render, redirect, get_object_or_404
from .forms import SiteParametersForm, ContentForm, FeaturesForm
from .models import SiteParameters, Content, Features
from django.urls import reverse
from django.http import HttpResponseRedirect

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
	if request.method == "POST":
		form = ContentForm(request.POST)
		if form.is_valid():
			content = form.save()
			return redirect('choose_features', params_pk = pk, content_pk = content.pk)
	else:
		form = ContentForm()
	return render(request, 'main/input_content.html', {'form': form})

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

	inf = inf.split('\r\n\r\n')

	content = get_object_or_404(Content, pk = content_pk)
	content = content.to_dict()

	page_features = {}
	for page in inf:
		page = page.split('\r\n')
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

	pages = ['main', 'about-us', 'features']
	for page in pages:
		features = dict()
		for line in page_features[page]:
			line = line.split(': ')
			features[line[0]] = line[1]
		turn_features_in_css_rules(styles, features, page)

	import os
	base_dir = os.path.dirname(os.path.abspath(__file__))
	styles = create_css(styles)

	with open(str.format("{0}\static\css\dynamic.css", base_dir), 'w') as file_obj:
		file_obj.write(styles)

	# content = {
	# 	'main':{
	# 		'logo': True,
	# 		'header': "Кухни из Германии",
	# 		'slogan': "ПОД ЗАКАЗ ОТ 4000 ЕВРО\nГАРАНТИЯ 5 ЛЕТ\nРАБОТАЕМ ПО ВСЕЙ БЕЛАРУСИ",
	# 	},
	# 	'about-us': {
	# 		'logo': None,
	# 		'single-position': None, # single-position: 'top' | 'bottom'
	# 		'header': 'O нас',
	# 		'paragraphs':[
	# 			{
	# 				'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc tortor elit, egestas quis tincidunt ac, varius quis arcu. Donec auctor felis sed nibh aliquam tempus et eu tellus. Quisque consectetur eu leo id tincidunt. Duis et urna leo. Morbi vestibulum id nunc id eleifend. Mauris neque nibh, pulvinar ut elementum eget, luctus at nisl.',
	# 				'image': None,
	# 			},
	# 		],
	# 	},
	# 	'features': {
	# 		'logo': None,
	# 		'single-position': None,
	# 		'header': 'Почему у нас?',
	# 		'paragraphs':[
	# 			{
	# 				'header': 'Качество',
	# 				'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
	# 				'image': None,
	# 			},
	# 			{
	# 				'header': 'Красота',
	# 				'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
	# 				'image': None,
	# 			},
	# 			{
	# 				'header': 'Удобство',
	# 				'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
	# 				'image': None,
	# 			},
	# 			{
	# 				'header': 'Престиж',
	# 				'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
	# 				'image': None,
	# 			},
	# 		],
	# 	},
	# }
	return render(request, 'main/success.html', { 'pages': pages, 'content': content })

def turn_features_in_css_rules(common_styles, features, page_name):
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
								'url({0})'.format(background) if '.' in background
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
						'background-image': features['fl-single-image'],
					},
				})

	common_styles.update(styles)

def create_css(styles):
	"""
	It returns a string that represents a css file
	THAT SHOULD BE OPTIMISED, CAUSE THIS CONCONTENTATE IMMUTABLE STR, THAT IS VERY SLOWLY
	"""
	css = ""
	for elem, style in styles.items():
		css += elem + ' {\n'

		#Данный участок кода временно исправляет то, что при добавлении правил из словаря
		#порядок правли нарушается, что критично для background
		background = True
		for feature, value in styles[elem].items():
			if 'background' in styles[elem] and background:
				css += str.format('\t{0}:{1};\n', 'background', styles[elem]['background'])
				background = False
			if feature == 'background':
				continue
		#################################################################################

			css += str.format('\t{0}:{1};\n', feature, value)
		css += '}\n\n'
	return css