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
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.utils.html import escape

from apps.v1api.utils import (build_fhir_profile,
                              date_to_iso)
from apps.v1api.views.fhir_elements import (human_name,
                                            )
from apps.v1api.views.practitioner import generate_fhir_profile


# def UnicodeDictReader(utf8_data, **kwargs):
#     # http://stackoverflow.com/questions/5004687/python-csv-dictreader-with-utf-8-data
#     csv_reader = csv.DictReader(utf8_data, **kwargs)
#     for row in csv_reader:
#         yield {key: str(value, 'utf-8') for key, value in row.iteritems()}


@staff_member_required
@login_required
def npi_index(request):
    # Show NPI Upload Home Page


    if settings.DEBUG:
        print(settings.APPLICATION_TITLE, "in apps.device.views.device_index")

    context = {'site' : Site.objects.get_current(),
              }
    return render_to_response('npi_upload/index.html',
                              RequestContext(request, context, ))


def npi_file_spec():
    """
     Return the NPI File spec from settings.
    :return:
    """

    #settings.NPI_SOURCE_FOLDER +

    file_name = settings.MEDIA_ROOT + settings.NPI_SOURCE_FILE

    return file_name


@staff_member_required
@login_required
def find_by_npi(request, record_no ):
    """
    :param request:
    :param profile,
    :param context (txn, guid)
    :return:
    """

    context = {}

    Txn =  {'resourceType' :"Practitioner",
            'display' :'Practitioner',
            'mask'  : True,
            'server': settings.FHIR_SERVER,
            'locn'  : "/baseDstu2/Practitioner",
            'template' : 'v1api/fhir_profile/practitioner',
            'extn'  : 'json.html',
            }

    practitioner = OrderedDict()

    context = {'txn'    : Txn,
               'record' : record_no,
               'search_by': "NPI"
               }

    f = npi_file_spec()

    delimiter = ','

    # Use next two counter values to control record processing
    # Allows blocks of records to be processed.

    rec_counter = 0
    #rec_counter = int(start)
    #end_rec_counter = int(stop)
    reader = OrderedDict()
    profile = OrderedDict()
    row_under = profile # passed in as OrderedDict()
    last_ten = 0

    message_content_update = {}
    message_content_skipped = {}

    # unicode, utf-8, iso-8859-1, latin-1, windows-1253, iso8859-7
    encode = "utf-8"

    with open(f,'r',
              encoding=encode,
              errors="surrogateescape") as fn:

        reader = csv.DictReader(fn,
                                delimiter = delimiter,
                                quotechar = '"')
        for row in reader:
            # print("Row: ",row )
            rec_counter += 1
            row_under = profile  # Passed in as OrderedDict()
            for fld_name in reader.fieldnames:
                # Write Fields in order of Fieldnames in CSV
                row_under[fld_name.replace(" ", "_").replace("(", "").replace(")", "").replace(".","")] = ""

                for key, value in row.items():
                    # We are now writing the field value to the new
                    # key dict
                    row_under[key.replace(" ", "_").replace("(", "").replace(")", "").replace(".","")] = value.decode('utf-8')

                    # if settings.DEBUG:
                    #     print(">>>>>>>>>>>>>>>>>")
                    #     print("Compiled Record:", row_under)
                    #     print(">>>>>>>>>>>>>>>>>")

            if row_under['NPI'] == record_no:

                profile_dict = generate_fhir_profile(request, context['txn']['resourceType'], row_under)

                # row_under['fhir_human_name'] = human_name({'use': "official",
                #                                            'prefix':[row_under['Provider_Name_Prefix_Text'],],
                #                                            'suffix':[row_under['Provider_Name_Suffix_Text'],],
                #                                            'family':[row_under['Provider_Last_Name_Legal_Name'],],
                #                                            'given' :[row_under['Provider_First_Name'],
                #                                                      row_under['Provider_Middle_Name'],],
                #                                           })
                if settings.DEBUG:
                    print("We found the NPI:",
                          row_under['NPI'],
                          "(", record_no, "/",
                          rec_counter, ")")

                context.update({'resourceType': context['txn']['resourceType'],
                                'profile': profile_dict,
                                'updated': date_to_iso(datetime.datetime.now()),
                           })

                fhir_profile = build_fhir_profile(request,
                                                  context,
                                                  context['txn']['template'],
                                                  context['txn']['extn'],
                                                  )
                if settings.DEBUG:
                    print("Profile:", fhir_profile)

                messages.info(request,"Found Record:"+str(rec_counter)+" with NPI:"+row_under['NPI'])
                # Update context with record
                context['profile'] = row_under
                break
            else:
                if settings.DEBUG:
                    print("Processing Record", rec_counter, row_under['NPI'])

    fn.close()

    return render_to_response('npi_upload/npi_source.html',
                              RequestContext(request, context,))


@staff_member_required
@login_required
def display_npi_source_record(request, record_no ):
    """
    :param request:
    :param profile,
    :param context (txn, guid)
    :return:
    """

    context = {}

    Txn =  {'resourceType' :"Practitioner",
            'display' :'Practitioner',
            'mask'  : True,
            'server': settings.FHIR_SERVER,
            'locn'  : "/baseDstu2/Practitioner",
            'template' : 'v1api/fhir_profile/practitioner',
            'extn'  : 'json.html',
            }

    practitioner = OrderedDict()

    if not record_no:
        record_no = 1
    else:
        record_no = int(record_no)

    context = {'txn'    : Txn,
               'record' : record_no,
               'search_by': "Row"
               }

    f = npi_file_spec()

    delimiter = ','

    # Use next two counter values to control record processing
    # Allows blocks of records to be processed.

    rec_counter = 0
    #rec_counter = int(start)
    #end_rec_counter = int(stop)
    reader = OrderedDict()
    profile = OrderedDict()
    row_under = profile # passed in as OrderedDict()
    last_ten = 0

    message_content_update = {}
    message_content_skipped = {}
    # unicode, utf-8, iso-8859-1, latin-1, windows-1253, iso8859-7
    encode = "utf-8"

    with open(f,'r',
              encoding=encode,
              errors="surrogateescape") as fn:
        reader = csv.DictReader(fn,
                                delimiter = delimiter,
                                quotechar = '"',
                                )
        for row in reader:
            # print("Row: ",row )
            rec_counter += 1

            if rec_counter > record_no:
                # Break out of the loop because we should have the record.
                break
            elif rec_counter < record_no:
                # Keep Looping
                pass

            elif rec_counter == record_no:
                # print("Row:    ", row)
                # print("=========================")
                # print("=========================")
                # print("=========================")

                row_under = profile  # Passed in as OrderedDict()
                for fld_name in reader.fieldnames:
                    # Write Fields in order of Fieldnames in CSV
                    row_under[fld_name.replace(" ",
                                               "_").replace("(",
                                                            "").replace(")",
                                                                        "").replace(".","")] = ""

                for key, value in row.items():
                    # We are now writing the field value to the new
                    # key dict

                    if isinstance(value, str):
                        if "�" in value:
                            #print("We have crap to deal with", "=======")
                            #print("Value:", value)
                            #print("Encoded Value:", value.encode('utf-8'))
                            #print("Str of encoded:", str(value.encode('utf-8').decode('utf-8')))
                            row_under[key.replace(" ",
                                                  "_").replace("(",
                                                               "").replace(")",
                                                                           "").replace(".","")] = value

                            pass
                        else:
                            row_under[key.replace(" ",
                                                  "_").replace("(",
                                                               "").replace(")",
                                                                           "").replace(".","")] = value
                    else:
                        row_under[key.replace(" ",
                                              "_").replace("(",
                                                           "").replace(")",
                                                                       "").replace(".","")] = value

                # if settings.DEBUG:
                #     print(">>>>>>>>>>>>>>>>>")
                #     print("Compiled Record:", row_under)
                #     print(">>>>>>>>>>>>>>>>>")

                profile_dict = generate_fhir_profile(request,
                                                     context['txn']['resourceType'],
                                                     row_under)


                context.update({'resourceType': context['txn']['resourceType'],
                                'source_row' : row_under,
                                'profile': profile_dict,
                                'updated': date_to_iso(datetime.datetime.now()),
                           })

                # row_under['fhir_human_name'] = human_name({'use': "official",
                #                                            'prefix':[row_under['Provider_Name_Prefix_Text'],],
                #                                            'suffix':[row_under['Provider_Name_Suffix_Text'],],
                #                                            'family':[row_under['Provider_Last_Name_Legal_Name'],],
                #                                            'given' :[row_under['Provider_First_Name'],
                #                                                      row_under['Provider_Middle_Name'],],
                #                                            })


                fhir_profile = build_fhir_profile(request,
                                                  context,
                                                  context['txn']['template'],
                                                  context['txn']['extn'],
                                                  )

                context['fhir_profile'] = fhir_profile

                if settings.DEBUG:
                    # print("Profile_DICT:", context['profile'])
                    #print("Profile:", fhir_profile)
                    pass

                messages.info(request,"Found Record:"+str(rec_counter)+" with NPI:"+row_under['NPI'])
                # Update context with record
                context['profile'] = profile_dict
                break

    fn.close()

    return render_to_response('npi_upload/npi_source.html',
                              RequestContext(request, context,))


@staff_member_required
@login_required
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
    ##        'locn'  : "/baseDstu2/Practitioner",
    #        'killlocn'  : "/delete?serverId=local&resource=Practitioner&resource-delete-id=",
    #        'template' : 'v1api/fhir_profile/practitioner',
    #        'extn'  : 'json.html',
    #        'DEADLY': True,
    #       }

    # We are constructing this url:
    # http://localhost:8080/fhir-p/
    # baseDstu2/Practitioner/{id}/
    # ?_format=json
    # in a DELETE transaction

    # http://fhir.bbonfhir.com:8080/fhir-p
    # /delete?serverId=local
    # &resource=Practitioner
    # &resource-delete-id=47604

    # Find the latest Update

    delete_result = {'deleted': 0,
                     'latestId': ""}

    if settings.DEBUG:
        print("In apps.npi_upload.views.delete_oldest with DEADLY=",
              (txn['DEADLY'] if 'DEADLY' in txn else "" ))

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
    # Do some setup for a delete transaction

    target_url = txn['server'] + txn['killlocn']
    post_param = "&_format=json"
    headers = {'Content-Type': 'application/json', 'Accept': 'text/plain'}

    # Find the latest update
    # Set delete_result['latestId'] to last updated record Id

    latest = {'id': "",
              'lastUpdated': ""}

    for item in search_result['duplicates']:
        # Loop through and check for latest update
        if settings.DEBUG:
            print("Key:", item.get('id'), " Date Field:", item.get('lastUpdated'))
        if item.get('lastUpdated') > latest.get('lastUpdated'):
            # Replace Latest with item
            latest = item
            print("Found Latest Record:",latest.get('id'))

    # Set the latest id in delete_result
    if latest.get('id'):
        delete_result['latestId'] = latest.get('id')

    # Loop through list - if not latest we delete entry
    for item in search_result['duplicates']:
        if not latest.get('id') == item.get('id'):
            # We have a record to delete
            delete_target = target_url + item.get('id') + post_param
            if settings.DEBUG:
                print("Delete Command:", delete_target)
            try:
                r = requests.delete(delete_target)
                # keep count of deletions
                if settings.DEBUG:
                    print("Returned:", r.status_code)
                    # print("result: " , r.text)
                delete_result['deleted'] = delete_result['deleted'] + 1

            except requests.ConnectionError:
                if settings.DEBUG:
                    print("Problem with connection on deletion", delete_target)
                messages.error(request,"Problem deleting:"+item.get('id'))


    # save deletions count to delete_result['delete']
    if settings.DEBUG:
        print("Delete result:", delete_result)
        print("Leaving apps.npi_upload.views.delete_oldest with DEADLY=",
              (txn['DEADLY'] if 'DEADLY' in txn else "" ))
    return delete_result


@staff_member_required
@login_required
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

    headers = {'Content-Type': 'application/json+fhir; charset=UTF-8',
               'Accept': 'text/plain'}

    try:
        r = requests.get(target_url)

        search_result['status_code'] = r.status_code
        if r.status_code == 200:
            # if settings.DEBUG:
            #    print("SEARCH result:  ", r.json())
            # we found something so get the content
            content = OrderedDict(r.json())
            # if settings.DEBUG:

                # print("SEARCH Content: ", content)
                # print("total:",content['total'])

            search_result['total'] = content['total']
            if search_result['total'] > 0:
                search_result['id'] = content['entry'][0]['resource']['id']
                search_result['versionId'] = content['entry'][0]['resource']['meta']['versionId']
                # if settings.DEBUG:
                #     print("id:", search_result['id'])
                search_result['duplicates'] = []
                for item in content['entry']:
                    #print("getting duplicates:", item['resource'])
                    #print(item['resource']['id'])
                    search_result['duplicates'].append({'id': item['resource']['id'],
                                                        'lastUpdated': item['resource']['meta']['lastUpdated']})
                # if settings.DEBUG:
                #     print("duplicates List:", search_result['duplicates'])
        if r.status_code == 404:
            print("Nothing found:[",r.status_code,"]" )

        messages.info(request, "found "+ str(search_result['total']) + " items.")

    except requests.ConnectionError:
        messages.error(request,"We had a problem reaching the fhir server")

    # if settings.DEBUG:
    #     print("Returning search_result", search_result)
    return search_result


@staff_member_required
@login_required
def get_npi(request, profile, context={}):
    """

    :param request:
    :param profile,
    :param context (txn, guid)
    :return:
    """

    # NPI File is defined in settings
    file_name = npi_file_spec()

    delimiter = ','

    # Use next two counter values to control record processing
    # Allows blocks of records to be processed.

    if context['txn']['start']:
        start = int(context['txn']['start'])
    else:
        start = 0

    if context['txn']['stop']:
        stop  = int(context['txn']['stop'])
    else:
        stop = 0

    rec_counter = 0
    end_rec_counter = int(stop)
    reader = OrderedDict()
    row_under = profile # passed in as OrderedDict()
    last_ten = 0

    message_content_update = {}
    message_content_skipped = {}

    # unicode, utf-8, iso-8859-1, latin-1, windows-1253, iso8859-7
    encode = "utf-8"

    with open(file_name,'r',
              encoding=encode,
              errors="surrogateescape") as fn:
        reader = csv.DictReader(fn,
                                delimiter = delimiter,
                                quotechar = '"')


        for row in reader:
            rec_counter += 1
            if rec_counter < start:
                if settings.DEBUG:
                    print(".", end="")
                continue
            row_under = profile # Passed in as OrderedDict()
            for fld_name in reader.fieldnames:
                # Write Fields in order of Fieldnames in CSV
                row_under[fld_name.replace(" ",
                                           "_").replace("(",
                                                        "").replace(")",
                                                                    "").replace(".","")] = ""

            for key, value in row.items():
                # We are now writing the field value to the new key dict
                # We need to deal with non-ascii crap in the input
                if isinstance(value, str):
                    value = value.encode('utf-8')
                row_under[key.replace(" ",
                                      "_").replace("(",
                                                   "").replace(")",
                                                               "").replace(".","")] = value.decode('utf-8')

            ###############
            # We have a record
            # Use a key field to search FHIR Profiles for matching key
            # For providers/practitioners this is NPI
            search_spec = {'namespace': "http://www.cms.gov",
                           'txn'  : context['txn'],
                           'field': "identifier",
                           'value': "NPI", # Field Name from Profile
                           }
            # if settings.DEBUG:
            #     print("Record:", rec_counter)
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
                    if search_result['total'] == 0:
                        # No record found so create one
                        row_under['mode'] = 'create'
                        row_under['versionId'] = "1"
                    elif search_result['total'] == 1:
                        # a record exists
                        row_under['mode'] = 'update'
                        if 'versionId' in search_result:
                            row_under['versionId'] = str(int(search_result['versionId']) + 1)
                        else:
                            row_under['versionId'] = "1"
                        if 'id' in search_result:
                            row_under['guid'] = search_result['id']
                    elif search_result['total']>= 2:
                        # We have duplicates
                        # if settings.DEBUG:
                        #     print("We have ",
                        #           len(search_result['duplicates']),
                        #           " duplicate(s)")
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
                                #if settings.DEBUG:
                                #    print("Deletion Results:", del_result)
                                ##########################
                    else:
                        row_under['mode'] = 'create'
                        row_under['versionId'] = "1"
            if not 'mode' in row_under:
                row_under['mode'] = 'create'
            if not 'versionId' in row_under:
                row_under['versionId'] = "1"

            #if settings.DEBUG:
            #    print("action:", row_under['mode'] + " ver:" + row_under['versionId'])

            # We will need to make this next piece generic
            # May be write_narrative(txn['resourceType'], row_under)
            # Then use resourceType to define Narrative format
            # row_under['narrative'] = write_practitioner_narrative(row_under)

            # if settings.DEBUG:
            #     print("row_under", row_under )
            #     print("Narrative:", row_under['narrative'])
            if "DEADLY" in context['txn']:
                if context['txn']['DEADLY'] == True:
                    pass
                    #if settings.DEBUG:
                    #    print("NOTHING TO DO WE ARE JUST DELETING DUPLICATES")
            elif row_under['Entity_Type_Code'] == '1':
                # if settings.DEBUG:
                #     print("Processing ", context['txn']['resourceType'])

                # Map input file fields for names to Human_Name section

                profile_dict = generate_fhir_profile(request,
                                                     context['txn']['resourceType'],
                                                     row_under)

                # row_under['fhir_human_name'] = human_name({'use': "official",
                #                                           'prefix':[row_under['Provider_Name_Prefix_Text'],],
                #                                           'suffix':[row_under['Provider_Name_Suffix_Text'],],
                #                                           'family':[row_under['Provider_Last_Name_Legal_Name'],],
                #                                           'given' :[row_under['Provider_First_Name'],
                #                                                    row_under['Provider_Middle_Name'],]
                #                                       })

                context.update({'resourceType': context['txn']['resourceType'],
                                'profile': profile_dict,
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

                if settings.DEBUG:
                    print("fhir_Profile:", fhir_profile)

                # Update the Fhir Server with this FHIR Profile

                target_url = context['txn']['server'] + context['txn']['locn']
                #if 'guid' in row_under and not row_under['mode'] == 'create':
                #    # If we have a guid and row_under['mode'] = 'update'
                #    target_url = target_url + "/" + row_under['guid']
                #target_url = target_url + "?_format=json"
                headers = {'Content-Type': 'application/json+fhir; charset=UTF-8',
                           'Accept'      : 'text/plain'}
                #if settings.DEBUG:
                #    print("request=",target_url)

                try:
                    if row_under['mode'] == 'create':
                        r = requests.post(target_url + "?_format=json",
                                          data=fhir_profile,
                                          headers=headers )
                    else:
                        r = requests.put(target_url + "/" + row_under['guid'] + "?_format=json",
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
                    if r.status_code == 400:
                        if settings.DEBUG:
                            print(r.status_code," Problem with input")
                            commit_data = r.__dict__
                            #commit_data = r.headers['content-location']
                            # print("Record Location:",
                            #      r.__dict__,
                            #      #r.headers['content-location'],
                            #      )
                            #print("ID:", commit_data)
                    if settings.DEBUG:
                        print(rec_counter,":","Mode:", row_under['mode'],"[",r.status_code,"] NPI:", row_under['NPI'],r.__dict__)
                    last_ten += 1
                    if last_ten == 10:
                        last_ten = 0
                    message_content_update[last_ten] = ["Mode:"+ row_under['mode'] + ":" + row_under['NPI'] + "[" + str(r.status_code) + "]"]

                    #if settings.DEBUG:
                    #    print("r:", r)

                except requests.ConnectionError:
                    messages.error(request,"Problem posting:" + row_under['NPI'])

                # if settings.DEBUG:
                #     print("Target:", target_url)


            else: # Not a Practitioner but an organization - Entity_Type=2
                #if settings.DEBUG:
                #    print(rec_counter," Skipping:", row_under['NPI'])
                last_ten += 1
                if last_ten == 10:
                    last_ten = 0
                message_content_skipped[rec_counter] = [row_under['NPI']]

            if rec_counter >end_rec_counter:
                break

    fn.close()

    str_message = ""
    for msg, value in message_content_update.items():
        str_message = str_message + str(msg) + ":" + str(message_content_update[msg])+". "
    skp_message = ""
    for msg, value in message_content_skipped.items():
        skp_message = skp_message + str(msg) + ":" + str(message_content_skipped[msg])+". "

    messages.info(request, "Last 10 records updated:" + str_message)
    messages.info(request, "Skipped:" + skp_message)
    context = {}
    if settings.DEBUG:
        print("Done")
    return message_content_update


@staff_member_required
@login_required
def write_fhir_practitioner(request, start, stop):
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

    if start:
        Txn['start'] = start
    else:
        Txn['start'] = 0

    if stop:
        Txn['stop'] = stop
    else:
        Txn['stop'] = 10


    practitioner = OrderedDict()

    context = {'txn' : Txn,
               }

    result = get_npi(request, profile=practitioner, context=context)

    # if settings.DEBUG:
    #     print("Result:", result)

    return render_to_response('npi_upload/index.html',
                              RequestContext(request, context,))


@staff_member_required
@login_required
def remove_duplicate_npi(request, start, stop):
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
            'killlocn'  : "/delete?serverId=local&resource=Practitioner&resource-delete-id=",
            'template' : 'v1api/fhir_profile/practitioner',
            'extn'  : 'json.html',
            'DEADLY': True,  # If DEADLY = True we will delete records
            }

    if start:
        Txn['start'] = start
    else:
        Txn['start'] = 0

    if stop:
        Txn['stop'] = stop
    else:
        Txn['stop'] = 10


    practitioner = OrderedDict()

    context = {'txn' : Txn,
               }

    result = get_npi(request, profile=practitioner, context=context)

    # if settings.DEBUG:
    #     print("Result:", result)

    return render_to_response('npi_upload/index.html',
                              RequestContext(request, context,))



