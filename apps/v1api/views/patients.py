"""
bbofuser: apps.v1api.views
FILE: patients
Created: 8/16/15 11:21 PM


"""
from django.contrib import messages

__author__ = 'Mark Scrimshire:@ekivemark'


import json
import requests

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

from apps.v1api.utils import (get_format, etree_to_dict,
                              xml_str_to_json_str)

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

    # Set Context
    context ={'display': Txn['display'],
              'name'   : Txn['name'],
              'mask'   : mask,
              'key'    : key,
              'fmt'    : fmt,
              'output' : "test output ",
              'args'   : args,
              'kwargs' : kwargs,
              'get'    : request.GET,
              'pass_to': pass_to,
              }
    try:
        r = requests.get(pass_to)

        if fmt == "xml":

            xml_text = minidom.parseString(r.text)
            print("XML_TEXT:", xml_text.toxml())
            root     = ET.fromstring(r.text)
            #root_out = etree_to_dict(r.text)

            json_string = ""
            #json_out = xml_str_to_json_str(r.text, json_string)
            if settings.DEBUG:
                print("Root ET XML:", root)
                #print("XML:", root_out)
                #print("JSON_OUT:", json_out,":", json_string)

            drill_down = ['Bundle',
                          'entry',
                          'Patient',]
            level = 0

            tag0 = xml_text.getElementsByTagName("text")
            #tag1 = tag0.getElementsByTagName("entry")

            print("Patient?:", tag0)
            print("DrillDown:", drill_down[level])
            print("root find:", root.find(drill_down[level]))
            for element in root:
                print("Child Element:", element)
                if drill_down[level] in element:
                    level+=1
                    for element2 in element:
                        print("Element2:", element2)
                        if drill_down[level] in element2:
                            print("Element2.iter()", element2.iter())
            text = root[4][0][0][2][1].findtext("text")

            pretty_xml = xml_text.toprettyxml()
            if settings.DEBUG:
                print("TEXT:", text)
                #print("Pretty XML:", pretty_xml)

            context['result'] = pretty_xml # convert
            context['text']   = pretty_xml

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

            context['result'] = r.json() # convert
            context['text']   = content['resource']['text']

        # Setup the page

        if settings.DEBUG:
            print()
            #print("Context:",context)

        return render_to_response(Txn['template'],
                              RequestContext(request,
                                             context,))

    except requests.ConnectionError:
        print("Whoops - Problem connecting to FHIR Server")
        messages.error(request,"FHIR Server is unreachable. Are you on the CMS Network?")
        return HttpResponseRedirect(reverse('api:v1:home'))
