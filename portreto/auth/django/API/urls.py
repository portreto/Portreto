from django.conf.urls import include, url
from . import views
from . import tests
from django.views.generic import RedirectView

app_name = 'API'

urlpatterns = [
    # GET /api/test/
    #url(r'^test/$', tests.test, name='tests'),

    # GET /api/
    url(r'^$', views.api, name='api'),

    # POST /api/token/<token>/
    url(r'^token/(?P<token>[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*)/$', views.token, name='token'),


    # TODO : Comment out
    # POST /create/token/
    url(r'^create/token/$', views.createToken, name='createToken'),

    # TODO : Comment out
    # POST /auth/token/
    url(r'^auth/token/$', views.authToken, name='authToken'),

    # POST /api/create/user/token/<token>
    url(r'^create/user/token/(?P<token>[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*)/$',
        views.create_user_by_token, name='create_user_by_token'),

    # TODO : Comment out or change
    # POST /api/create/user/
    url(r'^create/user/$',views.create_user_request, name='create_user_request'),

    # GET /api/create/
    #url(r'^create/$',views.create, name='create'),

    # POST /api/auth/user/token/<token>
    url(r'^auth/user/token/(?P<token>[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*)/$',
        views.auth_user_by_token, name='auth_user_by_token'),

    # TODO : Comment out or change
    # POST /api/auth/user/
    url(r'^auth/user/$',views.auth_user_request, name='auth_user_request'),
]
