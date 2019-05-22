from django.contrib import admin
from django.conf.urls import include, url

urlpatterns = [
    # auth/admin/
    url(r'^admin/', admin.site.urls),

    # auth/
    url(r'^', include('Service.urls')),

    # auth/api/
    url(r'^api/', include('API.urls')),

]
