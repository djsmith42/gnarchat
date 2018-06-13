from django.conf.urls import include, url
from django.urls import path

from django.contrib import admin
admin.autodiscover()

import website.views

urlpatterns = [
    url(r'^$', website.views.index, name='index'),
    url(r'^db', website.views.db, name='db'),
    path('admin/', admin.site.urls),
]
