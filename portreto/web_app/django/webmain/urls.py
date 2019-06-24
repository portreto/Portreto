from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from . import views

app_name = 'webmain'

urlpatterns = [
    url(r'^$', views.home_view, name='index'),
    url(r'^(?P<gallery_id>[0-9]+)/(?P<photo_id>[0-9]+)/$', views.photo_detail, name='photo_detail'),
    url(r'^(?P<gallery_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^create_gallery/$', views.create_gallery, name='create_gallery'),
    url(r'^search/$', views.search, name='search'), # TODO CHANGE THAT0
    url(r'^(?P<gallery_id>[0-9]+)/add_photo/$', views.add_photo, name='add_photo'),
    url(r'^(?P<gallery_id>[0-9]+)/like_gallery/(?P<redirect_target>[\w\-]+)/$', views.like_gallery, name='like_gallery'),
    url(r'^(?P<gallery_id>[0-9]+)/delete_gallery/$', views.delete_gallery, name='delete_gallery'),
    url(r'^(?P<gallery_id>[0-9]+)/update_gallery/$', views.update_gallery, name='update_gallery'),
    url(r'^(?P<gallery_id>[0-9]+)/comment_gallery/(?P<redirect_target>[\w\-]+)/$', views.comment_gallery, name='comment_gallery'),
    url(r'^(?P<gallery_id>[0-9]+)/delete_comment_gallery/(?P<comment_id>[0-9]+)/(?P<redirect_target>[\w\-]+)/$', views.delete_comment_gallery, name='delete_comment_gallery'),
    url(r'^(?P<photo_id>[0-9]+)/delete_comment_photo/(?P<comment_id>[0-9]+)$', views.delete_comment_photo, name='delete_comment_photo'),
    url(r'^(?P<photo_id>[0-9]+)/comment_photo/$', views.comment_photo, name='comment_photo'),
    url(r'^(?P<gallery_id>[0-9]+)/delete_photo/(?P<photo_id>[0-9]+)/$', views.delete_photo, name='delete_photo'),
    url(r'^(?P<gallery_id>[0-9]+)/update_photo/(?P<photo_id>[0-9]+)/$', views.update_photo, name='update_photo'),
    url(r'^(?P<gallery_id>[0-9]+)/(?P<photo_id>[0-9]+)/like_photo/$', views.like_photo, name='like_photo'), #TODO CHECK IF WE ARE GOING TO DO IT THAT WAY
    url(r'^follow/(?P<user_id>[0-9]+)/$', views.follow, name='follow'),
]

# if settings.DEBUG:
#     urlpatterns += staticfiles_urlpatterns()
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
