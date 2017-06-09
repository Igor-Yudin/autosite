from django.shortcuts import render, redirect, get_object_or_404
from .forms import SiteParametersForm, ContentForm
from .models import SiteParameters, Content, Features, PageFeatures
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.staticfiles.templatetags.staticfiles import static
from sklearn.externals import joblib
from colorsys import rgb_to_hls, hls_to_rgb
from PIL import Image
from io import BytesIO
import pandas as pd
import os
import requests


# Константные значения, отражающие шаблоны страниц
NONE = 0 # Тип не установлен
IMAGE = 1 # В качестве фона страницы используется изображение
COLOR = 2 # В качестве фона страницы использутеся цвет
COLORIMAGE = 3 # В качестве фона страницы используется цвет, страница содержит изображение
SEPHEADER = 4 # В качестве фона для загаловка используется изображение, для основного текста - белый цвет


# Корневая директория приложения внутри проекта
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class PatternType():
	"""
	Перечень типов страниц
	"""
	def __init__(self):
		self.Image = 1
		self.Color = 2
		self.ColorImage = 3
		self.SepHeader = 4


def input_parameters(request):
	"""
	Данное представление создает форму для ввода характеристик
	целевой аудитории и ключевых слов, производит ее валидацию.
	В случае успешно прохождения валидации сохраняет
	выбранные параметры в базе данных и перенаправляет на
	страницу ввода контента.
	"""
	if request.method == "POST":
		form = SiteParametersForm(request.POST)
		if form.is_valid():
			site_params = form.save()
			return redirect('input_content', pk=site_params.pk)
	else:
		form = SiteParametersForm()
	return render(request, 'main/input_parameters.html', {'form': form})

def input_content(request, pk):
	"""
	Данное представление создает форму для ввода контента страницы,
	произовдит валидацию введенного контента и в случае успеха
	перенаправляет на страницу выбора свойств страницы.
	"""
	form = ContentForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		content = form.save()
		return redirect('choose_features', params_pk=pk, content_pk=content.pk)
	else:
		return render(request, 'main/input_content.html', {'form': form, 'pk': pk})

def get_input_parameters(site_parameters):
	"""
	Формирует дата фрейм для прогнозирование, который
	соответствует введенным пользователем характеристикам
	целевой аудитории и ключевым словам.
	"""
	# Путь к файлу со списком ключевых слов
	path_to_file = '{0}/static/data/keywords.txt'.format(BASE_DIR)
	with open(path_to_file) as file_obj:
		keywords = file_obj.read()

	# Датафрейм с параметрами введенными пользователем
	# (если ключевое слово было выбрано - 1, иначе - 0)
	keywords_table = pd.DataFrame()

	# Инициализировать нулями
	for keyword in keywords.lower().split(','):
		keywords_table[keyword] = (0,)

	# Список выбранных пользователем ключевых слов
	choosen_keywords = site_parameters.keywords.lower().split(', ')

	# Отметить выбранные
	for keyword in choosen_keywords:
		keywords_table[keyword] = (1,)

	keywords_table['age'] = site_parameters.age
	keywords_table['gender'] = site_parameters.gender

	return keywords_table

def get_page_pattern_type(page, input_parameters):
	"""
	Функция для классификации типа страницы на основе введенных
	пользователем параметров
	"""
	# Путь к файлу с моделью классификации
	path_to_file = '{0}/static/data/{1}_type_clf.pkl'.format(BASE_DIR, page)
	clf = joblib.load(path_to_file)
	page_type = clf.predict(input_parameters)
	return page_type

def get_page_color(page, input_parameters):
	"""
	Функция для классификации цвета страницы
	по данным введенным пользователем
	"""
	# Путь к файлу с моделью
	path_to_file = '{0}/static/data/{1}_color_clf.pkl'.format(BASE_DIR, page)
	clf = joblib.load(path_to_file)

	# Получение параметров цвета hls
	h, l, s = clf.predict(input_parameters)[0]

	# Конвертация цвета из hls в rgb
	rgb = hls_to_rgb(h, l, s)

	def trim_bounds(x):
		x = x if x <= 255 else 255
		x = x if x >= 0 else 0
		return x

	rgb = map(trim_bounds, rgb)

	# Перевод значаний каналов в шестнадцатиричное значение
	rgb = map(lambda x: format(int(x), '02x'), rgb)
	return '#{rgb}'.format(rgb=''.join(rgb))

def get_images_urls(keys):
	url = 'https://1d931b481ffaebd16485:0cfcc2c5ae4283efe13ed2ec75d03d1611166071@api.shutterstock.com/v2/images/search'

	params = {
		'url': url,
		'keys': keys,
		'type': 'photo',
		'orientation': 'horizontal',
		'sort': 'popular',
	}

	r = requests.get('{url}?query={keys}&orientation={orientation}&image_type={type}&sort={sort}'.format(**params))

	images_urls = []
	if r.status_code == 200 and r.json().get('total_count'):
		images_urls = [img['assets']['preview']['url'] for img in r.json()['data']]
	else:
		print('Error: status code is {code}'.format(code = r.status_code))

	return images_urls

def get_image_url(images_urls, n):
	"""
	Функция для поиска наиболее релевантых фотографий на сайте
	shutterstock по ключевым словам, введенным пользователем
	"""

	image_url = ''
	if images_urls:
		if n < len(images_urls):
			image_url = images_urls[n]
		else:
			image_url = images_urls[n % len(images_urls)]
	return image_url

def get_font_colors(page_type, page_background):
	"""
	Данная функция вовзвращает значение цвета для
	загаловка и основного текста из расчета того, что
	цвет загаловка должен контрастировать с цветом фона, а
	цвет основного текста должен быть немного светлее цвета загаловка
	"""
	def get_background_color(background):
		"""
		Функция возвращает самый часто встречаемый цвет
		на изображении, если в качестве фона используется изображение
		или, если цвет, то его и возвращает.
		"""
		if '.' in background:
			response = requests.get(background)
			image = Image.open(BytesIO(response.content))

			# Получить центр изображения 
			center_width_half, center_height_half = image.width // 6, image.height // 10
			half_width, half_height = image.width // 2, image.height // 2

			# Границы центра изображения
			box = (half_width - center_width_half,
				   half_height - center_height_half,
				   half_width + center_width_half,
				   half_height + center_height_half)

			center_image = image.crop(box)

			# Частоты цветов
			colors_freq = {}

			for pixel_color in center_image.getdata():
				if colors_freq.get(pixel_color):
					colors_freq[pixel_color] += 1
				else:
					colors_freq[pixel_color] = 1

			# Выбор наиболее часто встречаемого цвета
			color = max(colors_freq, key = lambda color: colors_freq[color])

			# Убрать альфа-канал
			color = color[:-1] if len(color) > 3 else color

			# Вернуть цвет в формате rgb css
			return '#' + ''.join(format(channel, '02x') for channel in color)
		else:
			return background

	def get_color_seperating_for(color):
		"""
		Функция возвращает наиболее контрастный цвет для color
		"""

		# Получить кортеж со значениями каналов из строки формата css rgb
		a_color = color[1:]
		a_color = list(map(''.join, zip(* [iter(a_color)] * 2)))
		a_color = list(map(lambda x: int(x, 16), a_color))
		
		# Цвета, из которых выбираются наиболее контрастные
		colors = ((17, 17, 17), (255, 255, 255))

		# Разница для каждого цвета
		difs = []
		for b_color in colors:
			# Расчитать разницу для каждого цвета, как сумму квадратов расстояния для каждого канала
			dif = sum(map(lambda a, b: (a - b) ** 2, a_color, b_color))
			difs.append(dif)
		# Индекс цвета с наибольшей контрастностью
		ind = difs.index(max(difs))

		# Вернуть цвет в формате css rgb
		return '#' + ''.join(format(channel, '02x') for channel in colors[ind])

	def get_lighter_color(color):
		"""
		Возвращает немного более свтлое значение цвета,
		если это возможно.
		"""
		# Получить цвет, как кортеж значений каналов
		color = color[1:]
		color = list(map(''.join, zip(* [iter(color)] * 2)))
		color = list(map(lambda x: int(x, 16), color))

		# Увеличить значение цветов канала на 5, если это возможно
		lighter_color = list(map(lambda x: x + 5 if x + 5 <= 255 else 255, color))

		# Вернуть значение цвета в формает css rgb
		return '#' + ''.join(format(channel, '02x') for channel in lighter_color)

	background_color = get_background_color(page_background)
	h_color = get_color_seperating_for(background_color)

	if page_type == SEPHEADER:
		p_color = '#161616'
	else:
		p_color = get_lighter_color(h_color)
	return h_color, p_color

def choose_features(request, params_pk, content_pk):
	"""
	Функция для определения параметров страницы.
	Классифицирует параметры и перенаправляет
	на страницу с отображением результата.
	"""

	# 1. Произвести машинное обучение и выявить основные цвета: фона, текста. Размер и стиль
	# текста.
	# 2. По ключевым словам определить тему изображений, найти несколько фотографий для фона
	# и обычных картинок, при этом их цвет должен соответствовать выбранным, иначе заменить его цветом
	# 3. На этом контент заканчивается, передается дальше.

	# Параметры сайта, введенные пользоватем
	site_params = get_object_or_404(SiteParameters, pk=params_pk)

	# Входные параметры для обучения, полученные по введенным
	input_parameters = get_input_parameters(site_params)

	# Получить ключевые слова, которые будут использованы
	# для поиска картинок для страницы
	themes = site_params.keywords

	# Лист релевантных изображений
	images_urls = get_images_urls(themes)
	# Индекс изобржаения
	image_ind = 0

	features = Features()

	# Для каждой страницы определется тип, цвет, цвет загаловка
	# и цвет текста
	for page in ('main', 'about_good', 'about_us', 'contacts'):
		page_pattern_type = get_page_pattern_type(page, input_parameters)
		getattr(features, page).pattern_type = page_pattern_type

		page_color = get_page_color(page, input_parameters)
		getattr(features, page).color = page_color

		# Установить изображение для страницы, если
		# ее тип подразумевает наличие изображения
		page_image = None
		if page_pattern_type != COLOR:
			page_image = get_image_url(images_urls, image_ind)
			image_ind += 1
			getattr(features, page).image = page_image
			if not page_image:
				getattr(features, page).pattern_type = COLOR

		# Получить цвет загаловка и текста
		if page_pattern_type in (COLOR, COLORIMAGE):
			page_background = page_color
		else:
			page_background = page_image

		h_color, t_color = get_font_colors(page_pattern_type, page_background)
		getattr(features, page).header_color = h_color
		getattr(features, page).text_color = t_color

		# Установить размер текста для главной страницы
		if page == 'main':
			getattr(features, page).header_size = 120
			getattr(features, page).text_size = 48

	features.save()
	return redirect('show_page', params_pk = params_pk,
								 content_pk = content_pk,
								 features_pk = features.pk)

def show_page(request, params_pk, content_pk, features_pk):
	"""
	Данное представление формирует файл css и отображает страницу
	с введенным пользователем контентом и свойствами
	"""
	features = get_object_or_404(Features, pk = features_pk)
	content = get_object_or_404(Content, pk = content_pk)

	styles = create_styles(content, features)
	styles = create_css(styles)

	with open("{0}/static/css/dynamic.css".format(BASE_DIR), 'w') as file_obj:
		file_obj.write(styles)

	return render(request, 'main/show_page.html',
		{
			'content': content,
			'css': 'css/dynamic.css',
			'types': PatternType(),
			'pages': ('about_good', 'about_us', 'contacts'),
			'features': features,
		})

def create_styles(content, features):
	"""
	Возвращает словарь с набором css свойств для свойств
	"""
	styles = {

		# Общие стили

		'*': {
			'margin': '0px',
			'padding': '0px',
			'border': '0px',
			'font-size': '100%',
			'font': 'inherit',
			'vertical-align': 'baseline',
			'box-sizing': 'border-box',
		},

		# Шрифты

		'body': {
			'line-height': '1',
			'font-family': features.font_family,
		},

		'h1, h2': {
			'text-align': 'center',
		},

		'p': {
			'text-align': 'center',
		},

		# Размеры, позиции, отступы

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

		'.inf_block_wrapper h2': {
			'margin-bottom': '15vh',
		},

		'.single': {
			'margin-left': 'calc(100% / 5)',
			'width': '60%',
			'margin-top': '5vh',
			'border-radius': '70px',
		},

		# Цвета

		'.subheader': {
			'background': '#ffffff',
		},
	}

	# Здесь есть функция, которая делает (if getattr), которая
	# позволяет выставлять свойства только для выбранных страниц, я временно эту возможность убираю

	# Для каждой страницы формируется css свойства на основе 
	# автоматически выбранных свойств
	for page_name in ('main', 'about_good', 'about_us', 'contacts'):
		# if getattr(content, page, None):
		page_features = getattr(features, page_name, None)
		styles.update(turn_features_into_css_rules(page_features, page_name))
	# else:
	# 	styles.update(turn_features_into_css_rules('main', features))

	return styles

def turn_features_into_css_rules(page_features, page_name):
	"""
	Функция создает словарь, который есть css свойства для выбранных
	свойств для каждой страницы.
	Возвращает словарь css свойств для страницы.
	"""

	assert page_name in ["main", "about_us", "about_good", "contacts"], 'page_name is incorrect'
	assert isinstance(page_features, PageFeatures), "page_features is not an instance of PageFeatures"

	class_name = '.' + page_name
	header_class = class_name + ' h2' 
	text_class = class_name + ' p'

	
	page_pattern_type = page_features.pattern_type
	color = page_features.color
	image = page_features.image
	h_color = page_features.header_color
	t_color = page_features.text_color

	styles = {
		class_name: {
			'background': 'url(%s)' % image if page_pattern_type == IMAGE else color,
			'background-repeat': 'no-repeat',
			# Если постаить размер 100% 115%,
			# размер искажается, но это позволяет убрать ватермарк
			'background-size': 'cover',
			'background-position': 'center center',
			'background-attachment': 'scroll',
			# 'min-height': '20vh' if page == 'contacts' else '40vh',
		},

		header_class: {
			'color': h_color,
		},

		text_class: {
			'color': t_color,
		},
	}

	h_size = page_features.header_size
	t_size = page_features.text_size

	styles[header_class].update({
		'font-size': h_size,
	})

	styles[text_class].update({
		'font-size': t_size,
	})

	# Установить свойства для страницы, если ее тип
	# подразумевает отдельно оформленный загаловок
	if page_pattern_type == SEPHEADER:
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
	Возвращает строку с оформленными css свойствами
	"""
	css = ""
	for elem, style in sorted(styles.items()):
		css += elem + ' {\n'
		# Использется отсортированные свойства, чтобы предотвартить
		# переопределение узкими стилями общих, как background
		# и background-position
		for feature, value in sorted(styles[elem].items()):
			css += '\t{0}: {1};\n'.format(feature, value)
		css += '}\n\n'
	return css