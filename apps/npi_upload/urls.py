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
                       url(r'^$',
                           'apps.npi_upload.views.npi_index',
                           name='npi_home'),
                       url(r'^source_view/(?P<record_no>[-\w]+)/$',
                           'apps.npi_upload.views.display_npi_source_record',
                           name='source_view'),
                       url(r'^source_npi_view/(?P<record_no>[-\w]+)/$',
                           'apps.npi_upload.views.find_by_npi',
                           name='npi_view'),

                       url(r'^upload/(?P<start>[-\w]+)/(?P<stop>[-\w]+)/$',
                           'apps.npi_upload.views.write_fhir_practitioner',
                           name='upload'),
                       url(r'^deduplicate/(?P<start>[-\w]+)/(?P<stop>[-\w]+)/$',
                           'apps.npi_upload.views.remove_duplicate_npi',
                           name='deduplicate'),

                       url(r'^admin/', include(admin.site.urls)),

                       )
