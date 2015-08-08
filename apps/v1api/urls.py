"""
bbofuser: apps.v1api
FILE: urls.py
Created: 8/6/15 6:34 PM

We will call this from the apps.api namespace as v1

i.e. [Server_root]/api/v1/

"""
__author__ = 'Mark Scrimshire:@ekivemark'

# TODO: Implement REST API with pass through to FHIR Server

from django.conf.urls import (patterns,
                              include,
                              url)
from django.contrib import admin

from apps.v1api.views import *
from apps.device.views import device_authenticate
admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'apps.v1api.views.api_index',
                           name='home'),
                       url(r'^patient/(?P<key>\w+)/$',
                           'apps.v1api.views.patient',
                           name='patient'),

                       url(r'^admin/', include(admin.site.urls)),

                       )