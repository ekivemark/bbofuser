"""
bbofuser: apps.eob_upload
FILE: urls
Created: 8/18/15 4:08 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.conf.urls import (patterns,
                              include,
                              url)
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$',
                           'apps.eob_upload.views.eob_index',
                           name='home'),
                       url(r'^load/(?P<patient_id>[-\w]+)$',
                           'apps.eob_upload.views.load_eob',
                           name='load'),

                       url(r'^write/(?P<patient_id>[-\w]+)/(?P<bbj_in>[0-9A-Za-z_\-.]+)$',
                           'apps.eob_upload.views.write_eob',
                           name='write'),

                       url(r'^admin/', include(admin.site.urls)),

                       )
