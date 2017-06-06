from django.db import models

class SiteParameters(models.Model):
	"""
	Модель для хранения парметров сайта.
	"""
	BOTH = 1
	MALE = 2
	FEMALE = 3
	GENDERS = (
		(MALE, 'Мужчины'),
		(FEMALE, 'Женщины'),
		(BOTH, 'Мужчины и женщины'),
	)

	ADULT = 1
	YOUTH = 2
	CHILD = 3
	SENIOR = 4

	AGES = (
		(CHILD, '5-15'),
		(YOUTH, '15-25'),
		(ADULT, '25-55'),
	)

	keywords = models.TextField()
	gender = models.IntegerField(choices = GENDERS, default = 1)
	age = models.IntegerField(choices = AGES, default = 1)


default_font_family = 'Palatino, "Palatino Linotype", "Book Antiqua", "Hoefler Text", Georgia, "Lucida Bright", Cambria, Times, "Times New Roman", serif'


class Features(models.Model):
	"""
	Модель для хранения свойств страницы.
	"""
	NONE = 0
	COLOR = 1
	IMAGE = 2
	COLORIMAGE = 3
	SEPHEADER = 4

	PAGE_TYPES = (
		(COLOR, 'Color'),
		(IMAGE, 'Image'),
		(COLORIMAGE, 'Color and image'),
		(SEPHEADER, 'Seperate header'),
	)

	font_family = models.CharField(max_length = 250, default = default_font_family)
	h_size = models.IntegerField(default = 25)
	p_size = models.IntegerField(default = 12)

	main_type = models.IntegerField(choices = PAGE_TYPES,
								 default = COLOR)
	main_color = models.CharField(max_length = 7, default = '#ffffff')
	main_image = models.CharField(max_length = 1000, default = '')
	main_h_color = models.CharField(max_length = 30, default = 'black')
	main_h_size = models.IntegerField(default = 90)
	main_p_color = models.CharField(max_length = 30, default = 'black')
	main_p_size = models.IntegerField(default = 45)

	about_us_type = models.IntegerField(choices = PAGE_TYPES,
									 default = NONE)
	about_us_color = models.CharField(max_length = 7, default = '#ffffff')
	about_us_image = models.CharField(max_length = 1000, default = '')
	about_us_h_color = models.CharField(max_length = 30, default = 'black')
	about_us_p_color = models.CharField(max_length = 30, default = 'black')

	about_good_type = models.IntegerField(choices = PAGE_TYPES,
									   default = NONE)
	about_good_color = models.CharField(max_length = 7, default = '#ffffff')
	about_good_image = models.CharField(max_length = 1000, default = '')
	about_good_h_color = models.CharField(max_length = 30, default = 'black')
	about_good_p_color = models.CharField(max_length = 30, default = 'black')

	contacts_type = models.IntegerField(choices = PAGE_TYPES,
									 default = NONE)
	contacts_color = models.CharField(max_length = 7, default = '#ffffff')
	contacts_image = models.CharField(max_length = 1000, default = '')
	contacts_h_color = models.CharField(max_length = 30, default = 'black')
	contacts_p_color = models.CharField(max_length = 30, default = 'black')

default_name = 'Django'
default_slogan = 'Django makes it easier to build better Web apps more quickly and with less code.'
default_about_good_h = 'Meet Django'
default_about_good_text = 'Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of Web development, so you can focus on writing your app without needing to reinvent the wheel. It’s free and open source.'
default_about_us_h = 'About the Django Software Foundation'
default_about_us_text = 'Development of Django is supported by an independent foundation established as a 501(c)(3) non-profit. Like most open-source foundations, the goal of the Django Software Foundation is to promote, support, and advance its open-source project: in our case, the Django Web framework.'
default_contacts_h = 'Stay in the loop'
default_contacts_text = 'Subscribe to one of our mailing lists to stay up to date with everything in the Django community.'

class Content(models.Model):
	"""
	Модель для хранения контента страницы.
	"""
	name = models.CharField(max_length = 100, default = default_name)

	slogan = models.TextField(blank=True, default = default_slogan)

	logo = models.ImageField(
		upload_to = 'images',
		null = True,
		default = None,
		blank = True
	)

	about_good_header = models.CharField(blank = True, max_length = 150, default = default_about_good_h)
	about_good_text = models.TextField(blank = True, default = default_about_good_text)

	about_us_header = models.CharField(blank = True, max_length = 150, default = default_about_us_h)
	about_us_text = models.TextField(blank = True, default = default_about_us_text)

	contacts_header = models.CharField(blank = True, max_length = 150, default = default_contacts_h)
	contacts_text = models.TextField(blank = True, default = default_contacts_text)