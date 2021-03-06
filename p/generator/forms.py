from django import forms
from .models import SiteParameters, Content
from django.utils.translation import ugettext_lazy as _

CATEGORIES_NAMES = (
	'transport',
	'business',
	'food',
	'house',
	'sports',
	'game',
	'devices',
	'arts',
	'events',
	'musics',
	'education',
	'job',
	'connection',
	'life',
	'finances',
	'beauty',
	'innovations',
	'pets',
	'app',
	'services',
	'goods',
	'web',
	'health',
)

CATEGORIES = tuple(zip(CATEGORIES_NAMES, CATEGORIES_NAMES))

class SiteParametersForm(forms.ModelForm):
	keywords = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
										 choices=CATEGORIES,
										 label='Ключевые слова',
										 error_messages={
										 					'required': _('Необходимо указать хотя бы одно ключевое слово')
										 				})

	class Meta:
		model = SiteParameters
		fields = '__all__'
		labels = {
			'gender': _('Пол целевой аудитории'),
			'age': _('Возраст целевой аудитории'),
			'keywords': _('Ключевые слова'),
		}

	def clean_keywords(self):
		keywords = self.cleaned_data['keywords']
		if not keywords:
			raise forms.ValidationError('Необходимо выбрать хотя бы одно ключевое слово')
		return ', '.join(keywords)

class ContentForm(forms.ModelForm):
	class Meta:
		model = Content
		fields = '__all__'
		labels = {
			'name': _('Название кампании'),
			'slogan': _('Слоган'),
			'logo': _('Логотип'),
			'about_us_header': _('Информация о кампании (загаловок)'),
			'about_us_text': _('Информация о кампании (текст)'),
			'about_good_header': _('Информация о таваре/услуге (загаловок)'),
			'about_good_text': _('Информация о таваре/услуге (текст)'),
			'contacts_header': _('Контакты (загаловок)'),
			'contacts_text': _('Контакты (текст)'),
		}
		error_messages = {
			'name': {
				'required': _('Укажите название кампании'),
			},
		}