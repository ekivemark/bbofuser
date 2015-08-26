"""
bbofuser
FILE: main
Created: 8/25/15 8:10 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext


def bb_index(request):
    # Show NPI Upload Home Page


    if settings.DEBUG:
        print(settings.APPLICATION_TITLE, "in apps.getbb.views.bb_index")

    context = {'site' : Site.objects.get_current(),
              }
    return render_to_response('getbb/index.html',
                              RequestContext(request, context, ))

