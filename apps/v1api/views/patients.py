"""
bbofuser: apps.v1api.views
FILE: patients
Created: 8/16/15 11:21 PM


"""
from django.contrib import messages

__author__ = 'Mark Scrimshire:@ekivemark'


import json
import requests
import untangle

from collections import OrderedDict
from xml.dom import minidom

from xml.etree import ElementTree as ET

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe

from django.shortcuts import render, render_to_response
from django.template import RequestContext

from accounts.models import Crosswalk

from apps.v1api.utils import get_format

# TODO: Setup DJANGO REST Framework
# DONE: Apply user scope to FHIR Pass through
# DONE: Test Pass through to FHIR Server
# DONE: Create api:vi namespace in urls.py
# TODO: Detect url of accessing apps. Store in Connected_from of Device field
# TODO: Extract site domain from querying url in Connected_From


@login_required
def patient(request, key=1, *args, **kwargs):
    """

    :param request:
    :param args:
    :param kwargs:
    :return:

    """
    # DONE: Setup Patient API so that ID is not required
    # DONE: Do CrossWalk Lookup to get Patient ID
    if settings.DEBUG:
        print("Request User Beneficiary(Patient):", request.user)
    try:
        xwalk = Crosswalk.objects.get(user=request.user)
    except Crosswalk.DoesNotExist:
        messages.error(request, "Unable to find Patient ID")
        return HttpResponseRedirect(reverse('api:v1:home'))


    if settings.DEBUG:
        print("Request.GET :", request.GET)
        print("KWargs      :", kwargs)
        print("Crosswalk   :", xwalk)
        print("GUID        :", xwalk.guid)


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

    # Check for _format=
    fmt = get_format(request.GET)
    if settings.DEBUG:
        print("get_Format returned:", fmt)

    #fmt_type = "?_format=xml"
    #fmt_type = "?_format=json"

    fmt_type = "$everything?_format=" + fmt
    pass_to = pass_to + fmt_type
    mask_to = settings.DOMAIN

    try:
        r = requests.get(pass_to)

        if fmt == "xml":

            root = ET.fromstring(r.text)
            if settings.DEBUG:
                print("Root ET XML:", root)

            xml_text = minidom.parseString(r.text)
            pretty_xml = xml_text.toprettyxml()

            print("DOM:", xml_text.toxml())
            convert = untangle.parse(xml_text.toxml())

            #print("Elements:", xml_text._get_firstChild())
            bundle =  xml_text._get_firstChild()
            untangled = untangle.parse(r.text)
            child_name = untangled.Bundle.entry
            print("Bundle:", child_name)
            for element in child_name:
                print("child_item element:", child_name[element])

            #result = convert['name']
            print("Result:", result)
        else:

            convert = OrderedDict(r.json())
            # result = mark_safe(convert)

        if settings.DEBUG:
            print("Convert:", convert)
            #print("Next Level - entry:", convert['entry'])
            #print("\n ANOTHER Level- text:", convert['entry'][0])

        content = OrderedDict(convert['entry'][0])

        text = ""

        if settings.DEBUG:
            print("resourceType:", content['resource'] )
            print("text:", content['resource']['text'])

        context = {'display': Txn['display'],
                   'name'   : Txn['name'],
                   'mask'   : mask,
                   'key'    : key,
                   'output' : "test output ",
                   'args'   : args,
                   'kwargs' : kwargs,
                   'get'    : request.GET,
                   'pass_to': pass_to,
                   'result' : r.json(), # convert,
                   'text'   : content['resource']['text'],
                    }

        if settings.DEBUG:
            print()
            print("Context:",context)

        return render_to_response(Txn['template'],
                              RequestContext(request,
                                             context,))

    except requests.ConnectionError:
        print("Whoops - Problem connecting to FHIR Server")
        messages.error(request,"FHIR Server is unreachable. Are you on the CMS Network?")
        return HttpResponseRedirect(reverse('api:v1:home'))
