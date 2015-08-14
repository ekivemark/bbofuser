"""
bbofuser: apps.v1api
FILE: views.py
Created: 8/6/15 6:34 PM

Views for V1 of REST API
i.e. [Server_root]/api/v1/

"""
__author__ = 'Mark Scrimshire:@ekivemark'

import json

import requests
import xml.dom.minidom

from xml.etree import ElementTree

from django.conf import settings
from django.utils.safestring import mark_safe

from django.shortcuts import render, render_to_response
from django.template import RequestContext


# TODO: Setup DJANGO REST Framework
# DONE: Apply user scope to FHIR Pass through
# DONE: Test Pass through to FHIR Server
# DONE: Create api:vi namespace in urls.py
# TODO: Detect url of accessing apps. Store in Connected_from of Device field
# TODO: Extract site domain from querying url in Connected_From

# Create your views here.


def api_index(request):
    # Show API/v1 Home Page

    if settings.DEBUG:
        print(settings.APPLICATION_TITLE, "in apps.api.views.api_index")

    context = {}
    from django.template import RequestContext
    return render_to_response('v1api/index.html',
                              RequestContext(request, context, ))


def patient(request, key=1, *args, **kwargs):
    """

    :param request:
    :param args:
    :param kwargs:
    :return:

    """
# DONE: Setup Patient API so that ID is not required
# TODO: Do CrossWalk Lookup to get Patient ID

# DONE: Define Transaction Dictionary to enable generic presentation of API Call
    Txn =  {'name'  :"Patient",
            'display' :'Patient',
            'mask'  : True,
            'server': settings.FHIR_SERVER,
            'locn'  : "/baseDstu2/Patient/",
            'template' : 'v1api/patient.html',
             }

    mask = False
    if 'mask' in Txn:
        mask = Txn['mask']

    pass_to = Txn['server'] + Txn['locn']
    pass_to = pass_to + str(key)+"/"


    fmt = "json"

    #fmt_type = "?_format=xml"
    #fmt_type = "?_format=json"

    fmt_type = "$everything?_format=" + fmt
    pass_to = pass_to + fmt_type
    mask_to = settings.DOMAIN

    r = requests.get(pass_to)

    #xml_text = xml.dom.minidom.parseString(r.text)
    #result = xml_text.toprettyxml()

    convert = json.dumps(r.json())
    result = mark_safe(convert)



    context = {'display': Txn['display'],
               'name'   : Txn['name'],
               'mask'   : mask,
               'key'    : key,
               'output' : "test output ",
               'args'   : args,
               'kwargs' : kwargs,
               'get'    : request.GET,
               'pass_to': pass_to,
               'result' : convert,
               }

    print("Context:",context)

    return render_to_response(Txn['template'],
                              RequestContext(request,
                                             context,))