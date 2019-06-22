from django.urls import path
from . import views

app_name = 'webmain'

urlpatterns = [
    path('', views.index, name='index'),
]