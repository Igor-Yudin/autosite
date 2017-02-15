from django import forms
from .models import SiteParameters, ContentJson, Features, Content, SimplePage, SimplePageParagraph
from django.utils.translation import ugettext_lazy as _

class SiteParametersForm(forms.ModelForm):
	class Meta:
		model = SiteParameters
		fields = '__all__'
		labels = {
			'theme': _('Категория товаров или услуг'),
			'sex': _('Пол целевой аудитории'),
			'age': _('Возраст целевой аудитории'),
			'target': _('Группа основных покупателей'),
			'good_type': _('Что вы предлагаете'),
		}

class ContentJsonForm(forms.ModelForm):
	class Meta:
		model = ContentJson
		fields = ('text',)
		labels = {
			'text': _('Контент'),
		}

		help_texts = {
			'text': _('В данной форме показаны реальные данные для отображения'),
		}

class FeaturesForm(forms.ModelForm):
	class Meta:
		model = Features
		fields = ('text',)
		labels = {
			'text': _('Свойства'),
		}

		help_texts = {
			'text': _('Данные свойства используются для отображения и будут получаться машинным обучением')
		}

class ContentForm(forms.ModelForm):
	class Meta:
		model = Content
		fields = ('name', 'slogan', 'logo', 'background',)
		labels = {
			'name': _('Название компании'),
			'slogan': _('Слоган'),
			'logo': _('Логотип'),
			'background': _('Изображение для фона'),
		}

		# help_texts = {
		# 	'name': _('Название компании должно быть указано'),
		# 	'slogan': _('Не обязательно указывать'),
		# 	'logo': _('Не обязательно указывать'),
		# 	'background': _('Оставьте пустым для автоматичского заполнения фона'),
		# }

class SimplePageForm(forms.ModelForm):
	class Meta:
		model = SimplePage
		fields = ('header', 'background', 'single_image')
		labels = {
			'header': _('Загаловок страницы'),
			'background': _('Фон страницы'),
			'single_image': _('Главное изображение'),
		}

class SimplePageParagraphForm(forms.ModelForm):
	class Meta:
		model = SimplePageParagraph
		fields = ('header', 'text', 'background', 'image',)
		labels = {
			'header': _('Загаловок параграфа'),
			'text': _('Текст параграфа'),
			'background': _('Подложка'),
			'image': _('Иконка'),
		}