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
		fields = '__all__'
		labels = {
			'name': _('Название кампании'),
			'slogan': _('Слоган'),
			'logo': _('Логотип'),
			'about_us': _('Информация о кампании'),
			'about_good': _('Информация о таваре/услуге'),
			'contacts': _('Контакты'),
		}
		help_texts = {
			'name': _('Обязательно заполните данное поле!'),
			'slogan': _('Необязательно для заполнения'),
			'about_us': _('Необязательно для заполнения'),
			'about_good': _('Необязательно для заполнения'),
			'contacts': _('Необязательно для заполнения'),
		}

class FeaturesForm(forms.ModelForm):
	class Meta:
		model = Features
		fields = '__all__'