"""
bbofuser
FILE: views.py
Created: 8/18/15 4:10 PM

"""
__author__ = 'Mark Scrimshire:@ekivemark'

import csv
import datetime
import json
import requests

from uuid import uuid4

from collections import OrderedDict
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.utils.html import escape

from apps.v1api.utils import (build_fhir_profile,
                              date_to_iso)

def npi_index(request):
    # Show NPI Upload Home Page


    if settings.DEBUG:
        print(settings.APPLICATION_TITLE, "in apps.device.views.device_index")

    context = {}
    return render_to_response('npi_upload/index.html',
                              RequestContext(request, context, ))


def write_practitioner_narrative(profile):
    """
    Write a Practitioner Narrative section using the Practitioner Profile
    :param profile:
    :return: text string
    """

    narrative = "Welcome to my Practice..."

    narrative = profile['Provider_Name_Prefix_Text']+profile['Provider_First_Name']+" "+profile['Provider_Last_Name_Legal_Name']
    if profile['Provider_Name_Suffix_Text']:
        narrative = narrative + " "+profile['Provider_Name_Suffix_Text']
    narrative = narrative + ".<br>"
    narrative = narrative + "Tel:" + profile['Provider_Business_Practice_Location_Address_Telephone_Number']+"<br>"
    narrative = narrative + "Practice Address:<br>"
    narrative = narrative + profile['Provider_First_Line_Business_Practice_Location_Address']+"<br>"
    if profile['Provider_Second_Line_Business_Practice_Location_Address']:
        narrative = narrative +profile['Provider_Second_Line_Business_Practice_Location_Address']+"<br>"
    narrative = narrative + profile['Provider_Business_Practice_Location_Address_City_Name']+" "
    narrative = narrative + profile['Provider_Business_Practice_Location_Address_State_Name']+"<br>"
    narrative = narrative + profile['Provider_Business_Practice_Location_Address_Postal_Code']+"<br>"

    if settings.DEBUG:
        print("Narrative function:", narrative)

    return narrative


def get_npi(request, profile, context={}):
    """

    :param request:
    :param profile,
    :param context (txn, guid)
    :return:
    """

    dir = "/Users/mark/Downloads/NPPES_Data_Dissemination_August_2015.zip/NPPES_Data_Dissemination_August_2015"

    f = dir + "/" + "npidata_20050523-20150809.csv"

    dest_file = f

    delimiter = ','

    data_array = OrderedDict()
    data = {}
    counter = 0
    reader = OrderedDict()
    row_under = profile # passed in as OrderedDict()
    last_ten = 0

    message_content_update = {}
    message_content_skipped = {}

    with open(dest_file,'r') as dest_f:
        reader = csv.DictReader(dest_f,
                            delimiter = delimiter,
                            quotechar = '"')

        for row in reader:
            counter += 1
            row_under = profile # Passed in as OrderedDict()
            for fld_name in reader.fieldnames:
                # Write Fields in order of Fieldnames in CSV
                row_under[fld_name.replace(" ","_").replace("(","").replace(")","")] = ""

            for key, value in row.items():
                # We are now writing the field value to the new key dict
                row_under[key.replace(" ","_").replace("(","").replace(")","")] = value

            row_under['guid'] = str(uuid4().urn)[9:]
            row_under['mode'] = 'create'
            row_under['versionId'] = "1"
            row_under['narrative'] = write_practitioner_narrative(row_under)
            # if settings.DEBUG:
            #     print("row_under", row_under )
            #     print("Narrative:", row_under['narrative'])

            if row_under['Entity_Type_Code'] == '1':
                if settings.DEBUG:
                    print("Processing Provider")
                context.update({'resourceType': "Practitioner",
                                'profile': row_under,
                                'updated': date_to_iso(datetime.datetime.now()),
                           })
                # Format: 2015-06-09T00:04:55.757-04:00
                if settings.DEBUG:
                    print("iso time for updated:", context['updated'])

                fhir_profile = build_fhir_profile(request,
                                                  context,
                                                  "v1api/fhir_profile/practitioner",
                                                  "json.html")

                # if settings.DEBUG:
                    # print("fhir_Profile:", fhir_profile)

                # Update the Fhir Server with this FHIR Profile

                target_url = context['txn']['server'] + context['txn']['locn']+"?_format=json"
                headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
                if settings.DEBUG:
                    print("request=",target_url)

                try:
                    r = requests.post(target_url,
                                  data=fhir_profile,
                                  headers=headers )
                    if r.status_code == 201:
                        # POST was successful
                        # Get the id
                        commit_data = r.__dict__

                        print("Record Location:",
                              r.headers['content-location'])
                        print("ID:", commit_data)

                    last_ten += 1
                    if last_ten == 10:
                        last_ten = 0
                    message_content_update[last_ten] = [row_under['NPI'],row_under['guid']]

                    if settings.DEBUG:
                        print("r:", r)

                except requests.ConnectionError:
                    messages.error(request,"Problem posting:"+row_under['guid']+" / "+row_under['NPI'])

                if settings.DEBUG:
                    print("Target:", target_url)


            else: # Not a Practitioner but an organization - Entity_Type=2
                if settings.DEBUG:
                    print(counter," Skipping:", row_under['NPI'])
                last_ten += 1
                if last_ten == 10:
                    last_ten = 0
                message_content_skipped[counter] = [row_under['NPI']]

            if counter >8:
                break

    dest_f.close()
    messages.info(request, "Last 10 records updated:" + message_content_update)
    messages.info(request, message_content_skipped)
    context = {}
    print("Done")
    return message_content_update


def write_fhir_practitioner(request):
    """

    :param request:
    :return:
    """

    Txn =  {'resourceType' :"Practitioner",
            'display' :'Practitioner',
            'mask'  : True,
            'server': settings.FHIR_SERVER,
            'locn'  : "/baseDstu2/Practitioner",
            'template' : 'v1api/fhir_profile/practitioner.json.html',
            }


    practitioner = OrderedDict()


    context = {'txn' : Txn,
               }

    result = get_npi(request, profile=practitioner, context=context)

    if settings.DEBUG:
        print("Result:", result)

    return render_to_response('npi_upload/index.html',
                              RequestContext(request, context,))

