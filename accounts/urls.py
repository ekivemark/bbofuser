"""
 Developer Framework top level
"""
from django.conf.urls import (patterns,
                              include,
                              url)
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       # Examples:
                       url(r'^login$', 'accounts.views.sms.sms_login',
                           name='login'),
                       url(r'smscode/', 'accounts.views.sms.sms_code',
                           name='sms_code'),
                       url(r'^logout$', 'accounts.views.logout',
                           name='logout'),
                       url(r'^$', 'accounts.views.home_index',
                           name='home'),
                       url(r'^manage_account$',
                           'accounts.views.other.manage_account',
                           name='manage_account'),
                       url(r'^connect_application$',
                           'accounts.views.connect_application',
                           name='connect_application'),
                       url(r'^user/edit$', 'accounts.views.user.user_edit',
                           name='user_edit'),
                       url(r'^application/edit/(?P<pk>[-\w]+)/$',
                           'accounts.views.organization.application_edit',
                           name='application_edit'),

                       url(r'^admin/', include(admin.site.urls)),

                       # Manage Account
                       # Remove Account

                       )
