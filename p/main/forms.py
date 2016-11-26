from django import forms
from .models import SiteParameters, Content, Features
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

class ContentForm(forms.ModelForm):
	class Meta:
		model = Content
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
			'text': _('Пока указаны некоторые свойства')
		}