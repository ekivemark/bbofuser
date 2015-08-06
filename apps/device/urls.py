"""
bbofuser:device
FILE: urls
Created: 8/3/15 6:00 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.conf.urls import (patterns,
                              include,
                              url)
from django.contrib import admin

from apps.device.views import *

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'apps.device.views.device_index',
                           name='device_home'),
                       url(r'^add',
                            'apps.device.views.device_add',
                            name='device_add'),
                       url(r'^edit/(?P<pk>[-\w]+)/$',
                            'apps.device.views.device_edit',
                            name='device_edit'),
                       # url(r'^device/edit/(?P<pk>[-\w]+)/$',
                       #     'apps.device.views.device_edit',
                       #     name='device_edit'),
                       url(r'^delete/(?P<pk>[-\w]+)/$',
                            'apps.device.views.Device_Delete', name='device_delete'),
                       url(r'^login/$', 'apps.device.views.Device_Login',
                           name='device_login'),


                       url(r'^admin/', include(admin.site.urls)),

                       )
