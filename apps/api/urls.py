"""
bbofuser: api
FILE: urls
Created: 8/4/15 10:15 PM

Access to the FHIR API

"""
__author__ = 'Mark Scrimshire:@ekivemark'

# DONE: Implement REST API v1 (apps.v1api) napespace v1
# DONE: Build Authentication using Device Account

from django.conf.urls import (patterns,
                              include,
                              url)
from django.contrib import admin

from apps.api.views import *
from apps.device.views import device_authenticate
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$',
                           'apps.api.views.api_index',
                           name='home'),
                       url(r'^login$',
                           'apps.device.views.device_authenticate',
                           name='login'),
                       url(r'^v1/',
                           include('apps.v1api.urls',
                                   namespace='v1')),

                       url(r'^admin/', include(admin.site.urls)),

                       )
