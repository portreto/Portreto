from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'


urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<profile_username>[\w\-]+)/$', views.getProfile, name='getProfile'),
]