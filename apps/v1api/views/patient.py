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
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import (HttpResponseRedirect,
                         HttpResponse,
                         JsonResponse, )
from django.utils.safestring import mark_safe

from django.shortcuts import render, render_to_response
from django.template import RequestContext

from accounts.models import Crosswalk

from apps.v1api.utils import (get_format,
                              etree_to_dict,
                              xml_str_to_json_str,
                              get_url_query_string,
                              concat_string,
                              build_params)


# TODO: Setup DJANGO REST Framework
# DONE: Apply user scope to FHIR Pass through
# DONE: Test Pass through to FHIR Server
# DONE: Create api:vi namespace in urls.py.py
# TODO: Detect url of accessing apps. Store in Connected_from of Device field
# TODO: Extract site domain from querying url in Connected_From


@login_required
def get_patient(request, *args, **kwargs):
    """
    Display Patient Profile
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

    if xwalk.fhir_url_id == "":
        err_msg = ['Sorry, We were unable to find',
                   'your record', ]
        exit_message = concat_string("",
                                     msg=err_msg,
                                     delimiter=" ",
                                     last=".")
        messages.error(request, exit_message)
        return HttpResponseRedirect(reverse('api:v1:home'))

    if settings.DEBUG:
        print("Request.GET :", request.GET)
        print("KWargs      :", kwargs)
        print("Crosswalk   :", xwalk)
        print("GUID        :", xwalk.guid)
        print("FHIR        :", xwalk.fhir)
        print("FHIR URL ID :", xwalk.fhir_url_id)

    # We will deal internally in JSON Format if caller does not choose
    # a format
    in_fmt = "json"

    # DONE: Define Transaction Dictionary to enable generic presentation of API Call
    Txn = {'name': "Patient",
           'display': 'Patient',
           'mask': True,
           'server': settings.FHIR_SERVER,
           'locn': "/baseDstu2/Patient/",
           'template': 'v1api/patient.html',
           'in_fmt': in_fmt,
           }

    # Since this is BlueButton and we are dealing with Patient Records
    # We need to limit the id search to the specific beneficiary.
    # A BlueButton user should not be able to request a patient profile
    # that is not their own.
    # We do this via the CrossWalk. The xwalk.fhir_url_id is the patient
    # id as used in the url. eg. /Patient/23/
    # FHIR also allows an enquiry with ?_id=23. We need to detect that
    # and remove it from the parameters that are passed.
    # All other query parameters should be passed through to the
    # FHIR server.

    # Add URL Parameters to skip_parm to ignore or perform custom
    # processing with them. Use lower case values for matching.
    # DO NOT USE Uppercase
    skip_parm = ['_id', '_format']

    key = xwalk.fhir_url_id.strip()

    mask = False
    if 'mask' in Txn:
        mask = Txn['mask']

    pass_to = Txn['server'] + Txn['locn']
    pass_to = pass_to + key + "/"

    # We need to detect if a format was requested in the URL Parameters
    # ie. _format=json|xml
    # modify get_format to default to return nothing. ie. make no change
    # internal data handling will be JSON
    # _format will drive external display
    # if no _format setting  we will display in html (Current mode)
    # if valid _format string we will pass content through to display in
    # raw format

    get_fmt = get_format(request.GET)
    pass_to = pass_to + "?" + build_params(request.GET, skip_parm)

    mask_to = settings.DOMAIN

    # Set Context
    context = {'display': Txn['display'],
               'name': Txn['name'],
               'mask': mask,
               'key': key,
               'get_fmt': get_fmt,
               'in_fmt': Txn['in_fmt'],
               # 'output' : "test output ",
               # 'args'   : args,
               # 'kwargs' : kwargs,
               # 'get'    : request.GET,
               'pass_to': pass_to,
               }

    if settings.DEBUG:
        print("Calling Requests with:", pass_to)
    try:
        r = requests.get(pass_to)

        if get_fmt == "xml":

            xml_text = minidom.parseString(r.text)
            print("XML_TEXT:", xml_text.toxml())
            root = ET.fromstring(r.text)
            # root_out = etree_to_dict(r.text)

            json_string = ""
            # json_out = xml_str_to_json_str(r.text, json_string)
            if settings.DEBUG:
                print("Root ET XML:", root)
                # print("XML:", root_out)
                # print("JSON_OUT:", json_out,":", json_string)

            drill_down = ['Bundle',
                          'entry',
                          'Patient', ]
            level = 0

            tag0 = xml_text.getElementsByTagName("text")
            # tag1 = tag0.getElementsByTagName("entry")

            print("Patient?:", tag0)
            print("DrillDown:", drill_down[level])
            print("root find:", root.find(drill_down[level]))
            for element in root:
                print("Child Element:", element)
                if drill_down[level] in element:
                    level += 1
                    for element2 in element:
                        print("Element2:", element2)
                        if drill_down[level] in element2:
                            print("Element2.iter()", element2.iter())
            text = root[4][0][0][2][1].findtext("text")

            pretty_xml = xml_text.toprettyxml()
            if settings.DEBUG:
                print("TEXT:", text)
                # print("Pretty XML:", pretty_xml)

            context['result'] = pretty_xml  # convert
            context['text'] = pretty_xml

        else:

            convert = OrderedDict(r.json())
            # result = mark_safe(convert)

            if settings.DEBUG:
                print("Convert:", convert)
                # print("Next Level - entry:", convert['entry'])
                # print("\n ANOTHER Level- text:", convert['entry'][0])

            content = OrderedDict(convert)
            text = ""

            if settings.DEBUG:
                print("Content:", content)
                print("resourceType:", content['resourceType'])
                print("text:", content['text']['div'])

            context['result'] = r.json()  # convert
            context['text'] = content['text']['div']
            if 'error' in content:
                context['error'] = context['issue']

        # Setup the page

        if settings.DEBUG:
            print()
            # print("Context:",context)

        if get_fmt == 'xml' or get_fmt == 'json':
            if settings.DEBUG:
                print("Mode = ", get_fmt)
                print("Context['result']: ", context['result'])
            if get_fmt == "xml":
                return HttpResponse(context['result'],
                                    content_type='application/' + get_fmt)
            if get_fmt == "json":
                return JsonResponse(context['result'], )

        else:
            return render_to_response(Txn['template'],
                                      RequestContext(request,
                                                     context, ))

    except requests.ConnectionError:
        print("Whoops - Problem connecting to FHIR Server")
        messages.error(request,
                       "FHIR Server is unreachable. Are you on the CMS Network?")
        return HttpResponseRedirect(reverse('api:v1:home'))


@login_required
def get_eob(request, *args, **kwargs):
    """

    Display one or more EOBs but Always limit scope to Patient_Id

    :param request:
    :param eob_id:  Request a specific EOB
    :param args:
    :param kwargs:
    :return:
    """
    if settings.DEBUG:
        print("Request User Beneficiary(Patient):", request.user,
              "\nFor EOB Enquiry ")
    try:
        xwalk = Crosswalk.objects.get(user=request.user)
    except Crosswalk.DoesNotExist:
        messages.error(request, "Unable to find Patient ID")
        return HttpResponseRedirect(reverse('api:v1:home'))

    if xwalk.fhir_url_id == "":
        err_msg = ['Sorry, We were unable to find',
                   'your record', ]
        exit_message = concat_string("",
                                     msg=err_msg,
                                     delimiter=" ",
                                     last=".")
        messages.error(request, exit_message)
        return HttpResponseRedirect(reverse('api:v1:home'))

    if settings.DEBUG:
        print("Request.GET :", request.GET)
        print("KWargs      :", kwargs)
        print("Crosswalk   :", xwalk)
        print("GUID        :", xwalk.guid)
        print("FHIR        :", xwalk.fhir)
        print("FHIR URL ID :", xwalk.fhir_url_id)

    # We should have the xwalk.FHIR_url_id
    # So we will construct the EOB Identifier to include
    # This is a hack to limit EOBs returned to this user only.

    #   id_source['system'] = "https://mymedicare.gov/claims/beneficiary"
    #    id_source['use'] = "official"
    #    id_source['value'] = "Patient/"+str(patient_id)
    #    id_list.append(unique_id(id_source))

    # this search works:
    # http://fhir.bbonfhir.com:8080/fhir-p/
    # search?serverId=bbonfhir_dev
    # &resource=ExplanationOfBenefit
    # &param.0.0=https%3A%2F%2Fmymedicare.gov%2Fclaims%2Fbeneficiary
    # &param.0.1=Patient%2F4995401
    # &param.0.name=identifier
    # &param.0.type=token
    # &sort_by=
    # &sort_direction=
    # &resource-search-limit=

    # We will deal internally in JSON Format if caller does not choose
    # a format
    in_fmt = "json"
    get_fmt = get_format(request.GET)

    # DONE: Define Transaction Dictionary to enable generic presentation of API Call
    Txn = {'name': "ExplanationOfBenefit",
           'display': 'EOB',
           'mask': True,
           'server': settings.FHIR_SERVER,
           'locn': "/baseDstu2/ExplanationOfBenefit/",
           'template': 'v1api/eob.html',
           'in_fmt': in_fmt,
           }

    skip_parm = ['_id', '_format']

    key = xwalk.fhir_url_id.strip()

    mask = False
    if 'mask' in Txn:
        mask = Txn['mask']

    pass_to = Txn['server'] + Txn['locn']

    # We can allow an EOB but we MUST add a search Parameter
    # to limit the items found to those relevant to the Patient Id
    #if eob_id:
    #    pass_to = eob_id + "/"

    # Now apply the search restriction to limit to patient _id

    #pass_to = pass_to + key + "/"

    pass_to = pass_to + "?identifier="
    pass_to = pass_to + "https://mymedicare.gov/claims/beneficiary|"
    pass_to = pass_to + "Patient/"
    pass_to = pass_to + xwalk.fhir_url_id.strip()

    pass_to = pass_to + "&" + build_params(request.GET, skip_parm)
    if settings.DEBUG:
        print("Pass_to from build_params:", pass_to)

    if settings.DEBUG:
        print("Calling requests with pass_to:", pass_to)

    # Set Context
    context = {'display': Txn['display'],
               'name': Txn['name'],
               'mask': mask,
               'key': key,
               'get_fmt': get_fmt,
               'in_fmt': Txn['in_fmt'],
               # 'output' : "test output ",
               # 'args'   : args,
               # 'kwargs' : kwargs,
               # 'get'    : request.GET,
               'pass_to': pass_to,
               }

    try:
        r = requests.get(pass_to)

        if get_fmt == "xml":
            xml_text = minidom.parseString(r.text)
            pretty_xml = xml_text.toprettyxml()
            context['result'] = pretty_xml  # convert
            context['text'] = pretty_xml

            return HttpResponse(context['result'],
                                content_type='application/' + get_fmt)

        else: # get_fmt == "json" or None:

            convert = OrderedDict(r.json())
            # result = mark_safe(convert)

            if settings.DEBUG:
                print("Convert:", convert)

            content = OrderedDict(convert)
            text = ""

            context['result'] = r.json()  # convert
            if 'text' in content:
                context['text'] = content['resource']['text']['div']
            else:
                if settings.DEBUG:
                    print("Resource:", convert['entry'])
                context['text'] = convert['entry']

            if get_fmt == "json":
                return JsonResponse(context['result'], )

        return render_to_response(Txn['template'],
                                      RequestContext(request,
                                                     context, ))

    except requests.ConnectionError:
        print("Whoops - Problem connecting to FHIR Server")
        messages.error(request,
                       "FHIR Server is unreachable. "
                       "Are you on the CMS Network?")

    return HttpResponseRedirect(reverse('api:v1:home'))


@login_required
def get_eob_view(request, eob_id, *args, **kwargs):
    """

    Display one or more EOBs but Always limit scope to Patient_Id

    :param request:
    :param eob_id:  Request a specific EOB
    :param args:
    :param kwargs:
    :return:
    """
    if settings.DEBUG:
        print("Request User Beneficiary(Patient):", request.user,
              "\nFor Single EOB")
    try:
        xwalk = Crosswalk.objects.get(user=request.user)
    except Crosswalk.DoesNotExist:
        messages.error(request, "Unable to find Patient ID")
        return HttpResponseRedirect(reverse('api:v1:home'))

    if xwalk.fhir_url_id == "":
        err_msg = ['Sorry, We were unable to find',
                   'your record', ]
        exit_message = concat_string("",
                                     msg=err_msg,
                                     delimiter=" ",
                                     last=".")
        messages.error(request, exit_message)
        return HttpResponseRedirect(reverse('api:v1:home'))

    if settings.DEBUG:
        print("Request.GET :", request.GET)
        print("KWargs      :", kwargs)
        print("Crosswalk   :", xwalk)
        print("GUID        :", xwalk.guid)
        print("FHIR        :", xwalk.fhir)
        print("FHIR URL ID :", xwalk.fhir_url_id)

    # We should have the xwalk.FHIR_url_id
    # So we will construct the EOB Identifier to include
    # This is a hack to limit EOBs returned to this user only.

    #   id_source['system'] = "https://mymedicare.gov/claims/beneficiary"
    #    id_source['use'] = "official"
    #    id_source['value'] = "Patient/"+str(patient_id)
    #    id_list.append(unique_id(id_source))

    # this search works:
    # http://fhir.bbonfhir.com:8080/fhir-p/
    # search?serverId=bbonfhir_dev
    # &resource=ExplanationOfBenefit
    # &param.0.0=https%3A%2F%2Fmymedicare.gov%2Fclaims%2Fbeneficiary
    # &param.0.1=Patient%2F4995401
    # &param.0.name=identifier
    # &param.0.type=token
    # &sort_by=
    # &sort_direction=
    # &resource-search-limit=

    # We will deal internally in JSON Format if caller does not choose
    # a format
    in_fmt = "json"
    get_fmt = get_format(request.GET)

    # DONE: Define Transaction Dictionary to enable generic presentation of API Call
    Txn = {'name': "ExplanationOfBenefit",
           'display': 'EOB',
           'mask': True,
           'server': settings.FHIR_SERVER,
           'locn': "/baseDstu2/ExplanationOfBenefit/",
           'template': 'v1api/eob.html',
           'in_fmt': in_fmt,
           }

    skip_parm = ['_id', '_format']

    key = xwalk.fhir_url_id.strip()

    mask = False
    if 'mask' in Txn:
        mask = Txn['mask']

    pass_to = Txn['server'] + Txn['locn']

    # We can allow an EOB but we MUST add a search Parameter
    # to limit the items found to those relevant to the Patient Id
    if eob_id:
        pass_to = pass_to + eob_id + "/"

    # Now apply the search restriction to limit to patient _id

    #pass_to = pass_to + key + "/"

    pass_to = pass_to + "?identifier="
    pass_to = pass_to + "https://mymedicare.gov/claims/beneficiary|"
    pass_to = pass_to + "Patient/"
    pass_to = pass_to + xwalk.fhir_url_id.strip()

    pass_to = pass_to + "&" + build_params(request.GET, skip_parm)
    if settings.DEBUG:
        print("Pass_to from build_params:", pass_to)

    if settings.DEBUG:
        print("Calling requests with pass_to:", pass_to)

    # Set Context
    context = {'display': Txn['display'],
               'name': Txn['name'],
               'mask': mask,
               'key': key,
               'get_fmt': get_fmt,
               'in_fmt': Txn['in_fmt'],
               # 'output' : "test output ",
               # 'args'   : args,
               # 'kwargs' : kwargs,
               # 'get'    : request.GET,
               'pass_to': pass_to,
               }

    try:
        r = requests.get(pass_to)

        if get_fmt == "xml":
            xml_text = minidom.parseString(r.text)
            pretty_xml = xml_text.toprettyxml()
            context['result'] = pretty_xml  # convert
            context['text'] = pretty_xml

            return HttpResponse(context['result'],
                                content_type='application/' + get_fmt)

        else: # get_fmt == "json" or None:

            convert = OrderedDict(r.json())
            # result = mark_safe(convert)

            if settings.DEBUG:
                print("Convert:", convert)

            content = OrderedDict(convert)
            text = ""

            context['result'] = r.json()  # convert
            if 'text' in content:
                context['text'] = content['text']['div']
                if 'issue' in content:
                    context['error'] = content['issue']
            else:
                if settings.DEBUG:
                    print("Resource:", convert['entry'])
                context['text'] = convert['entry']

            if get_fmt == "json":
                return JsonResponse(context['result'], )

        return render_to_response(Txn['template'],
                                      RequestContext(request,
                                                     context, ))

    except requests.ConnectionError:
        print("Whoops - Problem connecting to FHIR Server")
        messages.error(request,
                       "FHIR Server is unreachable. "
                       "Are you on the CMS Network?")

    return HttpResponseRedirect(reverse('api:v1:home'))
