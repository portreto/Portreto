from django.urls import path
from . import views # dot is used to represent current directory

urlpatterns = [
    path('', views.home, name = 'portreto-home'),   #if we want to go to home page leave empty. PROBLEM WITH REGULAR EXPRESSIONS. Add name to reference patterns
    path('about/', views.about, name = 'portreto-about'),
]