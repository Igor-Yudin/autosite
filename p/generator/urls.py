from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.input_parameters, name='input_parameters'),
	url(r'^content/(?P<params_pk>\d+)/$', views.input_content, name = 'input_content'),
	url(r'^generated/(?P<params_pk>\d+)/(?P<content_pk>\d+)/(?P<features_pk>\d+)$', views.show_page, name='show_page'),
]