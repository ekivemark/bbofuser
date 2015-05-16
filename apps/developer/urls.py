"""
 Developer Framework top level
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from apps.developer.views import home_index, agree_to_terms, manage_account

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'developeraccount.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'apps.developer.views.home_index', name='home'),
    url(r'^register', 'apps.developer.views.agree_to_terms', name='agree_terms'),
    url(r'^manage_account', 'apps.developer.views.manage_account', name='manage_account'),

    url(r'^admin/', include(admin.site.urls)),

    # Manage Account
    # Remove Account
    # Add Associate User


)
