"""
 Developer Framework top level

"""
__author__ = 'mark'

"""
Resource views
 (c) 2015 - Mark Scrimshire - @ekivemark
"""

# TODO: Build REST API here
# TODO: Integrate REST framework

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
        print(application_title, "in resource.views.home_index")

    context = {"APPLICATION_TITLE": application_title}
    return render_to_response('index.html', RequestContext(request, context,))


