"""
 Developer views
 (c) 2015 - Mark Scrimshire - @ekivemark
"""

# TODO Activate Account
# TODO: Manage Account
# TODO: Delete Account
# TODO: Add Associate User (Link to Organization Account)
# TODO: Manage Organization
# TODO: Request Application Credentials
# TODO: Manage Application Credentials
# TODO: Delete Application Credentials
# TODO: accounts/profile Landing Page.

# Work flow will use django-registration to enable Account sign up
# After Activation
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
# Create your views here.

def home_index(request):

    # Show Home Page
    application_title = settings.APPLICATION_TITLE
    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print application_title, "in developer.views.home_index"

    context = {"APPLICATION_TITLE": application_title}
    return render_to_response('index.html', RequestContext(request, context,))


def agree_to_terms(request):

    # Agree to Terms
    application_title = settings.APPLICATION_TITLE
    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print application_title, "in developer.views.register"

    context = {"APPLICATION_TITLE": application_title}
    return render_to_response('developer/agree_to_terms.html', RequestContext(request, context,))


@login_required
def manage_account(request):

    # Manage Accounts entry page
    application_title = settings.APPLICATION_TITLE
    DEBuG = settings.DEBUG_SETTINGS

    if DEBuG:
        print application_title, "in developer.views.manage_account"

    context = {"APPLICATION_TITLE": application_title}
    return render_to_response('developer/manage_account.html', RequestContext(request, context,))
