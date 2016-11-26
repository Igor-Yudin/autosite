from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.new_page, name='new_page'),
	url(r'^content/(?P<pk>\d+)/$', views.input_content, name = 'input_content'),
	url(r'^features/(?P<params_pk>\d+)/(?P<content_pk>\d+)/$', views.choose_features, name = 'choose_features'),
	url(r'^generated/(?P<params_pk>\d+)/(?P<content_pk>\d+)/(?P<features_pk>\d+)$', views.show_page, name='show_page'),
]