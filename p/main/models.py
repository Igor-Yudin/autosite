from django.db import models

# Create your models here.

class SiteParameters(models.Model):
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
		(CHILD, '5 - 15'),
		(YOUTH, '15-25'),
		(ADULT, '25-55'),
		(SENIOR, '55+'),
	)

	keywords = models.TextField()
	gender = models.IntegerField(choices = GENDERS, default = 1)
	age = models.IntegerField(choices = AGES, default = 1)

class Features(models.Model):
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

	font_family = models.CharField(max_length = 250, default = 'Arial')
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

class Page(models.Model):
	"""
	Model for representing a page.
	"""
	IMAGE = 1
	COLOR = 2
	COLORIMAGE = 3
	SEPHEADER = 4

	PAGE_TYPES = (
		(IMAGE, 'Image'),
		(COLOR, 'Color'),
		(COLORIMAGE, 'Color and image'),
		(SEPHEADER, 'seperate header'),
	)
	page_type = models.IntegerField(choices = PAGE_TYPES, default = COLOR)

	header = models.CharField(max_length = 150)

	text = models.TextField()

class Content(models.Model):
	"""
	Model that represents all user-input content.
	"""
	name = models.CharField(max_length = 100)

	slogan = models.TextField(blank = True)

	logo = models.ImageField(
		upload_to = 'images',
		null = True,
		default = None,
		blank = True
	)

	about_good_header = models.CharField(blank = True, max_length = 150)
	about_good_text = models.TextField(blank = True)

	about_us_header = models.CharField(blank = True, max_length = 150)
	about_us_text = models.TextField(blank = True)

	contacts_header = models.CharField(blank = True, max_length = 150)
	contacts_text = models.TextField(blank = True)