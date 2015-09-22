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

from apps.subacc.views import *

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'apps.subacc.views.subacc_index',
                           name='home'),
                       url(r'^add',
                           'apps.subacc.views.subacc_add',
                            name='subacc_add'),
                       url(r'^edit/(?P<pk>[-\w]+)/$',
                           'apps.subacc.views.subacc_edit',
                            name='subacc_edit'),
                       # url(r'^subacc/edit/(?P<pk>[-\w]+)/$',
                       #     'apps.subacc.views.device_edit',
                       #     name='device_edit'),
                       url(r'^delete/(?P<pk>[-\w]+)/$',
                           'apps.subacc.views.Subacc_Delete', name='subacc_delete'),
                       url(r'^login/$',
                           'apps.subacc.views.Subaccount_Login',
                           name='subacc_login'),
                       url(r'^get_permission/$',
                           'apps.subacc.views.ask_user_for_permission',
                           name='ask_permission'),

                       url(r'^admin/', include(admin.site.urls)),

                       )
