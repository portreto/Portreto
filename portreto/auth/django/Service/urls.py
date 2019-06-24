from django.conf.urls import include, url
from . import views

app_name = 'Service'

urlpatterns = [

    # auth/
    url(r'^$', views.index, name='index'),

    # auth/service/
    url(r'^service$', views.index, name='index'),
]
