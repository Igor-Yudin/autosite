from django.contrib.staticfiles.templatetags.staticfiles import static
from django import template

register = template.Library()

@register.filter(name = 'linebreaksp')
def linebreaksp(text):
	"""
	Returns text with all new lines turned into p
	"""
	text = text.split('\n')
	return "".join(["<p>%s</p>" % block for block in text])

@register.filter(name='page')
def page(obj, page):
	"""
	Returns field for page
	"""
	return (obj, page)

@register.filter(name='attr')
def attr(obj_page, attr):
	obj, page = obj_page
	return getattr(obj, '{page}_{attr}'.format(page=page, attr=attr))