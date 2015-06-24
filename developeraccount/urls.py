from django.conf.urls import patterns, include, url
from django.conf import *
from registration.backends.default.urls import *
from django.contrib import admin
from accounts.forms.other import RegistrationFormTOSAndEmail
from django.contrib.auth import views as auth_views
from django.core.urlresolvers import reverse_lazy

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'developeraccount.views.home', name='home'),
    url(r'^$', 'accounts.views.home_index', name='home'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^demo/', include('apps.demo.urls', namespace='demo')),
    url(r'^registration/register/$', RegistrationView.as_view(form_class=RegistrationFormTOSAndEmail),
        name='register'),
    url(r'^registration/', include('registration.backends.default.urls')),
    url(r'^password/reset/$',auth_views.password_reset,
                           {'post_reset_redirect': reverse_lazy('password_reset_done')},
                           name='password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           name='password_reset_confirm'),
    url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           {'post_reset_redirect': reverse_lazy('password_reset_complete')},
                           name='password_reset_complete'),
    url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           name='password_reset_done'),

    url(r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
# TODO: Extend user model to enable organization
# TODO: Organization Approval (Test - Automatic)
# TODO: Organization Approval (Prod - Manual)
# TODO: Create Master User for Organization
# TODO: Create Standard User via master user
# TODO: Manage Developer Accounts
# TODO: Reassign Application Ownership within organization
# TODO: Delete accounts account
# TODO: Issue Application Key
# TODO: Manage Application Key
# TODO: Delete Application Key
# TODO: Create BlueButton User Api
# TODO: Change Organization Owner
# TODO: Add IsOwner Flag to User Account
# TODO: Study Bootstrap formatting
# TODO: Pre-load Sites 1 = PROD, 2=TEST 3=LOCALHOST
# TODO: Show date_joined in admin panel



