from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'


urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/(?P<username>[\w\-]+)/$', views.getProfile, name='getProfile'),
    # url(r'^search/', views.search , name='search'),
    # url(r'^profile/(?P<username>[-_\w.]+)/followers/$', views.followers, name='followers'),
    # url(r'^profile/(?P<username>[-_\w.]+)/following/$', views.following, name='following'),
    #path('accounts/register/', views.register, name='register'),
    #path('accounts/profile/', views.profile, name='profile'),
    #path('accounts/profile/delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
    #path('accounts/profile/favorite/<int:photo_id>/', views.favorite_photo, name='favorite_photo'),
    #path('accounts/profile/view/<int:photo_id>/favorite/', views.view_favorite_photo, name='view_favorite_photo'),

    #path('accounts/profile/import/', views.import_photo, name="import"),
    #path('accounts/profile/archive/', views.archive, name='archive'),

    #path('accounts/profile/view/<int:photo_id>/', views.view_photo, name="view_photo"),
    #path('accounts/profile/add/<int:photo_id>/', views.add_photo, name='add_photo'),
]
"""
path('', views.index_page, name='index_page'),

path('accounts/register/', views.register, name='register'),
path('accounts/profile/', views.profile, name='profile'),
path('accounts/profile/delete/<int:photo_id>/', views.delete_photo, name='delete_photo'),
path('accounts/profile/favorite/<int:photo_id>/', views.favorite_photo, name='favorite_photo'),
path('accounts/profile/view/<int:photo_id>/favorite/', views.view_favorite_photo, name='view_favorite_photo'),

path('accounts/profile/import/', views.import_photo, name="import"),
path('accounts/profile/archive/', views.archive, name='archive'),

path('accounts/profile/view/<int:photo_id>/', views.view_photo, name="view_photo"),
path('accounts/profile/add/<int:photo_id>/', views.add_photo, name='add_photo'),"""