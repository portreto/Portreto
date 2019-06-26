from django.conf.urls import url
from django.urls import path
from .views import *

urlpatterns = [
    path('', FilesView.as_view()),
    path('name/', NameView.as_view()),
]