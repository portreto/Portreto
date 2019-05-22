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


    url(r'^homepage/$', views.homepage, name='homepage'), #TODO : DELETE
    url(r'^page1/(?P<number1>[0-9]+)/$', views.page1, name='page1'), #TODO : DELETE
    url(r'^page2/(?P<number1>[0-9]+)/(?P<number2>[0-9]+)/$', views.page2, name='page2'), #TODO : DELETE
]