"""
bbofuser. uploader
FILE: urls.py
Created: 7/20/15 9:49 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',
                       # Examples:

                       url(r'^$', 'apps.uploader.views.home_index', name='home'),
                       url(r'^part_d_weekly$', 'apps.uploader.views.upload_part_d_weekly', name='partdweekly'),
                       url(r'^part_d_drug_extract$', 'apps.uploader.views.upload_drug_extract', name='partddrugextract'),
                       url(r'^admin/', include(admin.site.urls)),

                       )
