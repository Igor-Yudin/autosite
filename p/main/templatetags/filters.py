from django.contrib.staticfiles.templatetags.staticfiles import static
from django import template

register = template.Library()

@register.filter(name = 'page')
def page(queryset, page):
	return queryset.get(page_kind = page)

@register.filter(name = 'get_value')
def get_value(dictionary, key):
	return dictionary.get(key)

@register.filter(name = 'get_value_as_p')
def get_value_as_p(dictionary, key):
	return dictionary.get(key).as_p()

@register.filter(name = 'get_attr')
def get_attr(obj, attr):
	return getattr(obj, attr)

@register.filter(name = 'get_image_url')
def get_image_url(image_name):
	"""
	Returns string url(image_path)
	"""
	if image_name == None:
		return 'none'
	return "url(%s)" % static('images/' + image_name)

@register.filter(name = 'linebreaksp')
def linebreaksp(text):
	"""
	Returns text with all new lines turned into p
	"""
	text = text.split('\n')
	return "".join(["<p>%s</p>" % block for block in text])

@register.filter(name = 'get_static')
def get_static(filename):
	"""
	Returns url of dynamic css
	"""
	return static(filename)

@register.filter(name = 'concatenate')
def concatenate(s1, s2):
	"""
	Returns result of two strings concatenation.
	"""
	return s1 + s2