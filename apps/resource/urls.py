"""
 Developer Framework top level

"""
__author__ = 'mark'

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'bbonfhiruser.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^$', 'apps.resource.views.home_index', name='home'),

                       url(r'^admin/', include(admin.site.urls)),

                       # Manage Account
                       # Remove Account
                       # Add Associate User


                       )
