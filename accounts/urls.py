"""
 Developer Framework top level
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from registration.views import RegistrationView

from accounts.forms.other import RegistrationFormTOSAndEmail

from accounts.views import AgreementDetailView, \
    OrganizationDetailView, sms_code, sms_login

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^login$', 'accounts.views.sms_login', name='login'),
    url(r'smscode/', 'accounts.views.sms_code', name='sms_code'),
    url(r'^logout$', 'accounts.views.logout', name='logout'),
    url(r'^$', 'accounts.views.home_index', name='home'),
    url(r'^manage_account$', 'accounts.views.manage_account', name='manage_account'),
    url(r'^connect_organization$', 'accounts.views.connect_organization', name='connect_organization'),
    url(r'^connect_application$', 'accounts.views.connect_application', name='connect_application'),
    url(r'^agreement/(?P<slug>[-\w]+)/$', AgreementDetailView.as_view(), name='terms-detail'),
    url(r'^organization/(?P<slug>[-\w]+)/$', OrganizationDetailView.as_view(), name='organization-detail'),
    url(r'^admin/', include(admin.site.urls)),

    # Manage Account
    # Remove Account


)
