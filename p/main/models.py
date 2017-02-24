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
		(EDU, 'Образовательные услуги'),
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

class Features(models.Model):
	font_family = models.CharField(max_length = 250, default = 'Arial')
	header_size = models.IntegerField(default = 25)
	p_size = models.IntegerField(default = 12)

	main_background = models.CharField(max_length = 1000, default = '#ffffff')
	main_header_color = models.CharField(max_length = 30, default = 'black')
	main_header_size = models.IntegerField(default = 90)
	main_p_color = models.CharField(max_length = 30, default = 'black')
	main_p_size = models.IntegerField(default = 45)

	about_us_background = models.CharField(max_length = 1000, default = '#ffffff')
	about_us_header_color = models.CharField(max_length = 30, default = 'black')
	about_us_p_color = models.CharField(max_length = 30, default = 'black')

	about_good_background = models.CharField(max_length = 1000, default = '#ffffff')
	about_good_header_color = models.CharField(max_length = 30, default = 'black')
	about_good_p_color = models.CharField(max_length = 30, default = 'black')

	contacts_background = models.CharField(max_length = 1000, default = '#ffffff')
	contacts_header_color = models.CharField(max_length = 30, default = 'black')
	contacts_p_color = models.CharField(max_length = 30, default = 'black')

class Content(models.Model):
	"""
	Model that represents all user-input content.
	"""
	keywords = models.TextField()

	name = models.CharField(max_length = 100)

	slogan = models.TextField(blank = True)

	logo = models.ImageField(
		upload_to = 'images',
		null = True,
		default = None,
		blank = True
	)

	about_us = models.TextField(blank = True)

	about_good = models.TextField(blank = True)

	contacts = models.TextField(blank = True)