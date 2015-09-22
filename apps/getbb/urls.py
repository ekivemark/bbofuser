"""
bbofuser: apps.getbb
FILE: urls.py
Created: 8/6/15 6:34 PM

We will call this from the apps.api namespace as get_bb

i.e. [Server_root]/api/v1/

"""
__author__ = 'Mark Scrimshire:@ekivemark'

# TODO: Implement REST API with pass through to FHIR Server

from django.conf.urls import (patterns,
                              include,
                              url)
from django.contrib import admin

from apps.getbb.views.mym_login import *

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$',
                           'apps.getbb.views.main.bb_index',
                           name='home'),
#                       url(r'^connect/$',
#                           'apps.getbb.views.mym_login.connect',
#                           name='connect'),
                       url(r'^medicareconnect/$',
                           'apps.getbb.views.mym_login.connect_first',
                           name='connect_first'),

                       url(r'^disconnect/$',
                           'apps.getbb.views.mym_login.disconnect',
                           name='disconnect'),

                       url(r'^admin/', include(admin.site.urls)),

                       )