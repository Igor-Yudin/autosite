from django import forms
from .models import SiteParameters, ContentJson, Features
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