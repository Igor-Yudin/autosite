from django.db import models
import json

# Create your models here.
class SiteParameters(models.Model):
	EDU = 1
	BABY = 2
	SITE = 3
	CLOTH = 4
	OFF = 5

	THEMES = (
		(EDU, 'Образовательные устлуги'),
		(BABY, 'Товары для детей'),
		(SITE, 'Разработка сайтов'),
		(CLOTH, 'Одежда'),
		(OFF, 'Товары для офиса'),
	)

	MALE = 1
	FEMALE = 2
	BOTH = 3
	SEXES = (
		(MALE, 'Мужчины'),
		(FEMALE, 'Женщины'),
		(BOTH, 'Мужчины и женщины'),
	)

	CHILD = 1
	YOUTH = 2
	ADULT = 3
	SENIOR = 4

	AGES = (
		(CHILD, '5 - 15'),
		(YOUTH, '15-25'),
		(ADULT, '25-55'),
		(SENIOR, '55+'),
	)

	CLIENTS = 1
	BUISNESS = 2
	TARGET = (
		(CLIENTS, 'Клиенты'),
		(BUISNESS, 'Бизнес'),
	)

	GOOD = 1
	SERVICE = 2
	TYPE = (
		(GOOD, 'Продажа товара'),
		(SERVICE, 'Оказание услуги'),
	)

	theme = models.IntegerField(choices = THEMES, default = 1)
	sex = models.IntegerField(choices = SEXES, default = 1)
	age = models.IntegerField(choices = AGES, default = 1)
	target = models.IntegerField(choices = TARGET, default = 1)
	good_type = models.IntegerField(choices = TYPE, default = 1)

default_content = {
		'main':{
			'logo': True,
			'header': "Кухни из Германии",
			'slogan': "ПОД ЗАКАЗ ОТ 4000 ЕВРО\nГАРАНТИЯ 5 ЛЕТ\nРАБОТАЕМ ПО ВСЕЙ БЕЛАРУСИ",
		},
		'about-us': {
			'logo': None,
			'single-position': None, # single-position: 'top' | 'bottom'
			'header': 'O нас',
			'paragraphs':[
				{
					'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc tortor elit, egestas quis tincidunt ac, varius quis arcu. Donec auctor felis sed nibh aliquam tempus et eu tellus. Quisque consectetur eu leo id tincidunt. Duis et urna leo. Morbi vestibulum id nunc id eleifend. Mauris neque nibh, pulvinar ut elementum eget, luctus at nisl.',
					'image': None,
				},
			],
		},
		'features': {
			'logo': None,
			'single-position': None,
			'header': 'Почему у нас?',
			'paragraphs':[
				{
					'header': 'Качество',
					'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
					'image': None,
				},
				{
					'header': 'Красота',
					'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
					'image': None,
				},
				{
					'header': 'Удобство',
					'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
					'image': None,
				},
				{
					'header': 'Долговечность',
					'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
					'image': None,
				},
			],
		},
	}
import json
default_content = json.dumps(default_content)

class ContentJson(models.Model):
	text = models.TextField(default = default_content)

	def to_dict(self):
		return json.loads(self.text)

	def __str__(self):
		return json.dumps(self.text)

class Image(models.Model):
	image = models.ImageField(
		upload_to = 'images',
		null = True,
		blank = True,
		default = None
		)

default_features = """main
attachment: scroll
page-height: 100vh
background: images/main.jpg
logo: images/l.png
logo-width: 189
logo-height: 136
logo-position: top left
font-size: 22px
header-size: 45px
font-family: 'Arial'
font-color: #dbdbdb
inf-block-width: 75%
inf-block-align: center
inf-block-v-align: center
main-text-size: 90px
main-text-color: white
effects: darken
header-color: white
columns: none

about_us
attachment: fixed
page-height: 100vh
background: white
effects: none
font-family: 'Arial'
header-size: 30px
header-color: #121113
main-text-size: 90px
main-text-color: #121113
font-size: 14px
font-color: #8c8783
inf-block-width: 60%
inf-block-align: center
inf-block-v-align: center
columns: 1
fl-bl-text-align: center
fl-bl-header-align: center
fl-image-position: top
fl-block-background: none
fl-single-image: none
fl-image-form: square

features
attachment: fixed
page-height: 100vh
background: white
effects: none
font-family: 'Arial'
header-size: 30px
header-color: #121113
main-text-size: 90px
main-text-color: black
font-size: 14px
font-color: #8c8783
inf-block-width: 60%
inf-block-align: center
inf-block-v-align: to-top
columns: 2
fl-bl-text-align: center
fl-bl-header-align: center
fl-image-position: top
fl-block-background: none
fl-single-image: none
fl-image-form: square"""

class Features(models.Model):
	text = models.TextField(default = default_features)

class Content(models.Model):
	"""
	Model for representing content.
	"""

	# Order
	order = models.CharField(
		max_length = 200,
		blank = False
	)

	# Main page content
	name = models.CharField(
		max_length = 100,
		blank = False
	)

	slogan = models.TextField(default = None)
	
	logo = models.ImageField(
		upload_to = 'images',
		null = True,
		blank = True,
		default = None
	)
	
	background = models.ImageField(
		upload_to = 'images',
		null = True,
		blank = True,
		default = None
	)

	# Pages, like about-us, features, catalog have the same structure,
	# so all of them are represents by one model SimplePage,
	# instances of whick have foreignkey to Content.

	# Pages, like form, nav, footer have its personal structure, so
	# they should be represented by their own classes.

class SimplePage(models.Model):
	"""
	Model for representing simple pages.
	"""
	content = models.ForeignKey(
		Content,
		on_delete = models.CASCADE,
		related_name = 'pages'
	)

	page_kind = models.CharField(
		max_length = 15,
		blank = False
	)

	header = models.CharField(
		max_length = 100,
		blank = True,
		null = True,
		default = None
	)

	background = models.ImageField(
		upload_to = 'images',
		null = True,
		blank = True,
		default = None
	)

	single_image = models.ImageField(
		upload_to = 'images',
		null = True,
		blank = True,
		default = None
	)

	# Simple page has some paragraphs represented by class SimplePageParagraph

class SimplePageParagraph(models.Model):
	"""
	Model for representing simple page paragraphs.
	"""
	page = models.ForeignKey(
		SimplePage,
		on_delete = models.CASCADE,
		related_name = 'paragraphs'
	)

	header = models.CharField(
		max_length = 100,
		blank = True,
		null = True,
		default = None
	)

	text = models.TextField()

	background = models.ImageField(
		upload_to = 'images',
		null = True,
		blank = True,
		default = None
	)

	image = models.ImageField(
		upload_to = 'images',
		null = True,
		blank = True,
		default = None
	)