"""
 Developer Framework top level
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin

from accounts.views.other import AgreementDetailView, OrganizationDetailView, OrgApplication_Detail

from accounts.views.sms import sms_code, sms_login, login_optional_sms, login_optional
from accounts.views.user import user_edit
from accounts.views.organization import Organization_EditForm, OrgApplication_EditForm

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    #url(r'^login_alt$', 'accounts.views.sms.login_optional', name='login_sms'),
    #url(r'^login_alt$', 'accounts.views.sms.login_optional_sms', name='login_sms'),
    url(r'^login$', 'accounts.views.sms.sms_login', name='login'),
    url(r'smscode/', 'accounts.views.sms.sms_code', name='sms_code'),
    url(r'^logout$', 'accounts.views.logout', name='logout'),
    url(r'^$', 'accounts.views.home_index', name='home'),
    url(r'^manage_account$', 'accounts.views.other.manage_account', name='manage_account'),
    url(r'^connect_organization$', 'accounts.views.connect_organization', name='connect_organization'),
    url(r'^connect_application$', 'accounts.views.connect_application', name='connect_application'),
    url(r'^agreement/(?P<slug>[-\w]+)/$', AgreementDetailView.as_view(), name='terms-detail'),
    url(r'^organization/(?P<slug>[-\w]+)/$',
        OrganizationDetailView.as_view(),
        name='organization-detail'),
    url(r'^user/edit$', 'accounts.views.user.user_edit', name='user_edit'),
    url(r'^organization/edit$', 'accounts.views.organization.organization_edit',
        name='organization_edit'),
   url(r'^application/edit/(?P<pk>[-\w]+)/$', 'accounts.views.organization.orgapplication_edit',
        name='orgapplication_edit'),

    url(r'^admin/', include(admin.site.urls)),

    # Manage Account
    # Remove Account

    #TODO: Restructure SMSCode to come after login and check for mfa setting

)
