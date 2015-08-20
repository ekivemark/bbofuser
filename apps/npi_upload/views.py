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
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.utils.html import escape

from apps.v1api.utils import (build_fhir_profile,
                              date_to_iso)

@login_required()
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
    # Use <br/> to force line breaks. <br> will not validate successfully

    narrative = "Welcome to my Practice..."

    narrative = profile['Provider_Name_Prefix_Text']+profile['Provider_First_Name']+" "+profile['Provider_Last_Name_Legal_Name']
    if profile['Provider_Name_Suffix_Text']:
        narrative = narrative + " "+profile['Provider_Name_Suffix_Text']
    narrative = narrative + ".<br/>"
    narrative = narrative + "Tel:" + profile['Provider_Business_Practice_Location_Address_Telephone_Number']+"<br/>"
    narrative = narrative + "Practice Address:<br/>"
    narrative = narrative + profile['Provider_First_Line_Business_Practice_Location_Address']+"<br/>"
    if profile['Provider_Second_Line_Business_Practice_Location_Address']:
        narrative = narrative +profile['Provider_Second_Line_Business_Practice_Location_Address']+"<br/>"
    narrative = narrative + profile['Provider_Business_Practice_Location_Address_City_Name']+" "
    narrative = narrative + profile['Provider_Business_Practice_Location_Address_State_Name']+"<br/>"
    narrative = narrative + profile['Provider_Business_Practice_Location_Address_Postal_Code']+"<br/>"

    # if settings.DEBUG:
    #     print("Narrative function:", narrative)

    return narrative


def delete_oldest(request, resourceType, txn, search_result):
    """
    Get the duplicates list from search_result
    and delete all but oldest duplicate record.
    :param request:
    :param resourceType:
    :param search_result:
    :return:
    """

    # txn =  {'resourceType' :"Practitioner",
    #        'display' :'Practitioner',
    #        'mask'  : True,
    #        'server': settings.FHIR_SERVER,
    #        'locn'  : "/baseDstu2/Practitioner",
    #        'template' : 'v1api/fhir_profile/practitioner',
    #        'extn'  : 'json.html',
    #        'DEADLY': True,
    #       }

    # We are constructing this url:
    # http://localhost:8080/fhir-p/
    # baseDstu2/Practitioner/{id}/
    # ?_format=json
    # in a DELETE transaction

    # Find the latest Update

    delete_result = {'deleted': 0,
                     'latestId': ""}

    if not 'duplicates' in search_result:
        return delete_result

    if   len(search_result['duplicates']) == 0:
        # Nothing to do
        return delete_result
    elif len(search_result['duplicates']) == 1:
        # One or less duplicates - so nothing to do
        delete_result['latestId'] = search_result['duplicates'][0][0]
        if settings.DEBUG:
            print("delete_result:", delete_result)
        return delete_result

    # We have entries to delete
    # Find the latest update
    # Set delete_result['latestId'] to last updated record Id

    latest = {'id': "",
              'lastUpdated': ""}

    for key in search_result['duplicates']:
        # Loop through and check for latest update
        if key[1]:
            print("key:", key)
            print("id:", key[0],":", key[1])


    # Loop through list - if not latest we delete entry
    # keep count of deletions

    # save deletions count to delete_result['delete']

    return delete_result


def find_profile(request, resourceType, profile, search_spec):
    """
    Search a profile for an item
    :param request:
    :param resourceType:
    :param profile:
    :param search_spec:
    :return: dict with matched values
    """

    # We are constructing this url:
    # http://localhost:8080/fhir-p/
    # baseDstu2/Practitioner
    # ?identifier=http://www.cms.gov|1215930367
    # &_format=json


    # search_spec = {'namespace': "http://www.cms.gov",
    #                        'txn'  : context['txn'],
    #                        'field': "identifier",
    #                        'value': "NPI", # Field Name from Profile
    #                        }
     # txn =  {'resourceType' :"Practitioner",
     #        'display' :'Practitioner',
     #        'mask'  : True,
     #        'server': settings.FHIR_SERVER,
     #        'locn'  : "/baseDstu2/Practitioner",
     #        'template' : 'v1api/fhir_profile/practitioner',
     #        'extn'  : 'json.html',}

    search_result = {}

    search_q = "?" + search_spec['field'] + "="

    if 'namespace' in search_spec:
        search_q = search_q + search_spec['namespace'] + "|"

    search_q = search_q + profile[search_spec['value']]
    search_q = search_q + "&_format=json"

    target_url = search_spec['txn']['server'] + search_spec['txn']['locn'] + search_q

    headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

    try:
        r = requests.get(target_url)

        search_result['status_code'] = r.status_code
        if r.status_code == 200:
            # we found something so get the content
            content = OrderedDict(r.json())
            # if settings.DEBUG:
                # print("SEARCH result:  ", r.json())
                # print("SEARCH Content: ", content)
                # print("total:",content['total'])

            search_result['total'] = content['total']
            if search_result['total'] > 0:
                search_result['id'] = content['entry'][0]['resource']['id']
                search_result['versionId'] = content['entry'][0]['resource']['meta']['versionId']
                # if settings.DEBUG:
                #    print("id:", search_result['id'])
                search_result['duplicates'] = []
                for item in content['entry']:
                    #print("getting duplicates:", item['resource'])
                    #print(item['resource']['id'])
                    search_result['duplicates'].append({item['resource']['id'],
                                                        item['resource']['meta']['lastUpdated']})
                # if settings.DEBUG:
                #     print("duplicates List:", search_result['duplicates'])
        if r.status_code == 404:
            print("Nothing found:[",r.status_code,"]" )

        messages.info(request, "found "+ str(search_result['total']) + " items.")

    except requests.ConnectionError:
        messages.error(request,"We had a problem reaching the fhir server")


    return search_result


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

    # Use next two counter values to control record processing
    # Allows blocks of records to be processed.
    rec_counter = 0
    end_rec_counter = 9
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
            rec_counter += 1
            row_under = profile # Passed in as OrderedDict()
            for fld_name in reader.fieldnames:
                # Write Fields in order of Fieldnames in CSV
                row_under[fld_name.replace(" ","_").replace("(","").replace(")","")] = ""

            for key, value in row.items():
                # We are now writing the field value to the new key dict
                row_under[key.replace(" ","_").replace("(","").replace(")","")] = value

            ###############
            # We have a record
            # Use a key field to search FHIR Profiles for matching key
            # For providers/practitioners this is NPI
            search_spec = {'namespace': "http://www.cms.gov",
                           'txn'  : context['txn'],
                           'field': "identifier",
                           'value': "NPI", # Field Name from Profile
                           }
            search_result = find_profile(request,
                                         context['txn']['resourceType'],
                                         row_under,
                                         search_spec)

            if settings.DEBUG:
                print("Search Result:", search_result)
            # should return:
            #    search_result['status_code'] = r.status_code
            #    search_result['total'] = r.content['total']
            #    search_result['id'] = r.content['entry']['resource']['id']
            #    search_result['versionId'] = r.content['entry']['resource']['meta']['versionId']


            #row_under['guid'] = str(uuid4().urn)[9:]
            if 'status_code' in search_result:
                if search_result['status_code'] == 404:
                    row_under['mode'] = 'create'
                    row_under['versionId'] = "1"

                elif search_result['status_code'] == 200:
                    # Search can return no results with a
                    # status_code of 200. in which case total = 0
                    if search_result['total']>0:
                        # a record exists
                        row_under['mode'] = 'update'
                        row_under['versionId'] = str(int(search_result['versionId']) + 1)
                        row_under['guid'] = search_result['id']
                    elif search_result['total']>1:
                        # We have duplicates
                        if settings.DEBUG:
                            print("We have ",
                                  len(search_result['duplicates']),
                                  " duplicates")
                        # find the latest updates in the list to keep
                        # delete the rest
                        if 'DEADLY' in context['txn']:
                            # We have the Delete Command
                            if context['txn']['DEADLY'] == True:
                                del_result = delete_oldest(request,
                                                           context['txn']['resourceType'],
                                                           context['txn'],
                                                           search_result,
                                                          )
                                ##########################
                                ##########################
                                #
                                # Back from Delete function
                                #
                                ##########################
                    else:
                        row_under['mode'] = 'create'
                        row_under['versionId'] = "1"
            if settings.DEBUG:
                print("action:", row_under['mode'] + " ver:" + row_under['versionId'])

            # We will need to make this next piece generic
            # May be write_narrative(txn['resourceType'], row_under)
            # Then use resourceType to define Narrative format
            row_under['narrative'] = write_practitioner_narrative(row_under)

            # if settings.DEBUG:
            #     print("row_under", row_under )
            #     print("Narrative:", row_under['narrative'])

            if row_under['Entity_Type_Code'] == '1':
                # if settings.DEBUG:
                #     print("Processing ", context['txn']['resourceType'])
                context.update({'resourceType': context['txn']['resourceType'],
                                'profile': row_under,
                                'updated': date_to_iso(datetime.datetime.now()),
                           })
                # Format: 2015-06-09T00:04:55.757-04:00
                # if settings.DEBUG:
                #     print("iso time for updated:", context['updated'])

                fhir_profile = build_fhir_profile(request,
                                                  context,
                                                  context['txn']['template'],
                                                  context['txn']['extn'],
                                                  )

                # if settings.DEBUG:
                    # print("fhir_Profile:", fhir_profile)

                # Update the Fhir Server with this FHIR Profile

                target_url = context['txn']['server'] + context['txn']['locn']
                if 'guid' in row_under:
                    # If we have a guid and row_under['mode'] = 'update'
                    target_url = target_url + "/" + row_under['guid']
                target_url = target_url + "?_format=json"
                headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}
                #if settings.DEBUG:
                #    print("request=",target_url)

                try:
                    r = requests.post(target_url,
                                  data=fhir_profile,
                                  headers=headers )
                    if r.status_code == 201:
                        # POST was successful
                        # Get the id
                        # commit_data = r.__dict__
                        commit_data = r.headers['content-location']
                        # print("Record Location:",
                        #      r.headers['content-location'])
                        # print("ID:", commit_data)

                    last_ten += 1
                    if last_ten == 10:
                        last_ten = 0
                    message_content_update[last_ten] = [row_under['NPI']+"["+str(r.status_code)+"]"]

                    #if settings.DEBUG:
                    #    print("r:", r)

                except requests.ConnectionError:
                    messages.error(request,"Problem posting:"+row_under['NPI'])

                # if settings.DEBUG:
                #     print("Target:", target_url)


            else: # Not a Practitioner but an organization - Entity_Type=2
                if settings.DEBUG:
                    print(rec_counter," Skipping:", row_under['NPI'])
                last_ten += 1
                if last_ten == 10:
                    last_ten = 0
                message_content_skipped[rec_counter] = [row_under['NPI']]

            if rec_counter >end_rec_counter:
                break

    dest_f.close()

    str_message = ""
    for msg, value in message_content_update.items():
        str_message = str_message + str(msg)+":"+str(message_content_update[msg])+". "
    skp_message = ""
    for msg, value in message_content_skipped.items():
        skp_message = skp_message + str(msg)+":"+str(message_content_skipped[msg])+". "

    messages.info(request, "Last 10 records updated:" + str_message)
    messages.info(request, "Skipped:"+ skp_message)
    context = {}
    if settings.DEBUG:
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
            'template' : 'v1api/fhir_profile/practitioner',
            'extn'  : 'json.html',
            }

    practitioner = OrderedDict()

    context = {'txn' : Txn,
               }

    result = get_npi(request, profile=practitioner, context=context)

    # if settings.DEBUG:
    #     print("Result:", result)

    return render_to_response('npi_upload/index.html',
                              RequestContext(request, context,))


def remove_duplicate_npi(request):
    """
    Remove duplicate NPI Entries
    :param request:
    :return:

    We will find the NPI.
    Get the total
    Find all the entries by Id
    put the Ids in a list
    Find the highest number (Latest entry)
    cycle through the list and if not latest delete the record

    """

    # set up the transaction

    # call find_profile

    Txn =  {'resourceType' :"Practitioner",
            'display' :'Practitioner',
            'mask'  : True,
            'server': settings.FHIR_SERVER,
            'locn'  : "/baseDstu2/Practitioner",
            'template' : 'v1api/fhir_profile/practitioner',
            'extn'  : 'json.html',
            'DEADLY': True,  # If DEADLY = True we will delete records
            }

    practitioner = OrderedDict()

    context = {'txn' : Txn,
               }

    result = get_npi(request, profile=practitioner, context=context)

    # if settings.DEBUG:
    #     print("Result:", result)

    return render_to_response('npi_upload/index.html',
                              RequestContext(request, context,))



