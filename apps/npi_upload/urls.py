"""
bbofuser: apps.npi_upload
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
                       url(r'^$', 'apps.npi_upload.views.npi_index',
                           name='npi_home'),
                       url(r'^upload',
                            'apps.device.views.upload',
                            name='upload'),

                       url(r'^admin/', include(admin.site.urls)),

                       )
