"""
bbofuser:api
FILE: views
Created: 8/3/15 6:54 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.conf import settings
from django.shortcuts import (render,
                              render_to_response)
from django.template import RequestContext

# DONE: Login_Required Decorator for Device Accounts
# TODO: Setup DJANGO REST Framework
# TODO: Apply user scope to FHIR Passthrough
# TODO: Test Passthrough to FHIR Server
# TODO: Create api namespace in urls.py
# TODO: Detect url of accessing apps. Store in Connected_from of Device field
# TODO: Extract site domain from querying url in Connected_From
# DONE: Create API Landing Page (Unauthenticated)

def api_index(request):
    # Show API Home Page

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print(settings.APPLICATION_TITLE, "in apps.api.views.api_index")

    context = {}
    return render_to_response('api/index.html',
                              RequestContext(request, context, ))



