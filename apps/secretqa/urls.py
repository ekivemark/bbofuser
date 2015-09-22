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

from apps.secretqa.views import *

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^$', 'apps.secretqa.views.secretqa_index',
                           name='security_home'),
                       url(r'^add',
                            'apps.secretqa.views.secretqa_add',
                            name='security_add'),
                       url(r'^edit$',
                            'apps.secretqa.views.secretqa_edit',
                            name='security_edit'),

                       url(r'^pop_answer/(?P<qa>[-\w]+)/$',
                           'apps.secretqa.views.pop_answer',
                           name='security_pop_answer'),

                       # url(r'^subacc/edit/(?P<pk>[-\w]+)/$',
                       #     'apps.subacc.views.device_edit',
                       #     name='device_edit'),

                       #url(r'^delete(?P<pk>[-\w]+)/$',
                       #     SecretQA_Delete.as_view(), name='security_delete'),

                       url(r'^admin/', include(admin.site.urls)),

                       )
