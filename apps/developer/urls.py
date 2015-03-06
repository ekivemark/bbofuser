"""
 Developer Framework top level
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from .views import home_index

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'developeraccount.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'$', 'apps.developer.views.home_index', name='home'),
    url(r'^register', 'apps.developer.views.agree_to_terms', name='agree_terms'),
    url(r'^admin/', include(admin.site.urls)),

    # Manage Account
    # Remove Account
    # Add Associate User


)
