# -*- coding: utf-8 -*-
"""
bbofuser: eob_upload
FILE: views
Created: 9/3/15 12:27 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

import datetime
import json
import requests

from collections import OrderedDict
from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from accounts.models import User, Crosswalk

from apps.bluebutton.cms_parser import (cms_file_read,
                                        cms_text_read,
                                        parse_lines)
from apps.eob_upload.forms import BlueButtonJsonForm
from apps.npi_upload.views import find_profile
from apps.v1api.utils import (date_to_iso,
                              concat_string,
                              build_fhir_profile)
from apps.v1api.views.fhir_elements import (human_name,
                                            contact_point,
                                            address,
                                            unique_id)

@staff_member_required
@login_required
def eob_index(request):
    # Show NPI Upload Home Page


    if settings.DEBUG:
        print(settings.APPLICATION_TITLE, "in apps.eob_upload.views.eob_index")

    context = {'site' : Site.objects.get_current(),
              }
    return render_to_response('eob_upload/index.html',
                              RequestContext(request, context, ))


@login_required
def load_eob(request, patient_id):
    """

    Receive a Patient_Id and a CMS BlueButton file converted to JSON
     Using the json converter:
     https://github.com/ekivemark/python-bluebutton

    :param request:
    :param patient_id:
    :param bb_file:
    :return:
    """

    # Handle file upload
    if request.method == 'POST':
        form = BlueButtonJsonForm(request.POST, request.FILES)
        if form.is_valid():
            bbj_in = request.FILES['bbjfile']
            if settings.DEBUG:
                print("File Name: ", bbj_in)

            # Redirect to the write process
            return HttpResponseRedirect('/eob_upload/write/'+
                                        patient_id +'/'+str(bbj_in))
        else:
            form = BlueButtonJsonForm()  # empty, unbound form

    bbj_in = ""
    documents = bbj_in
    form = BlueButtonJsonForm()

    return render_to_response('eob_upload/upload.html',
                              {'documents': documents,
                               'patient_id': patient_id,
                               'form': form}, context_instance=RequestContext(request)
                              )


def json_to_eob(request):
    """

    :param request:
    :param patient_id:

    :return:
    """
    result = {}
    result['result'] = "FAIL"

    # if settings.DEBUG:
    #     print("Patient_Id =", patient_id)

    u = User.objects.get(email=request.user.email)
    x_walk = Crosswalk.objects.get(user=u)
    guid = x_walk.guid

    json_stuff = x_walk.mmg_bbjson
    if not json_stuff:
        result['reason'] = "Nothing to process"
        messages.info(request,result['reason'])

        return result

    if not x_walk.fhir_url_id:
        # No fhir_url_id so we need to create a patient profile
        outcome = create_patient(request, bb_dict=json_stuff)
        x_walk = Crosswalk.objects.get(user=u)

        if not x_walk.fhir_url_id:
            # create_patient failed to create a patient profile
            result['reason'] = "A patient profile was not created"
            messages.error(request, result['reason'])
            return result

    if settings.DEBUG:
        print("Converted BlueButton File:\n",
              json_stuff,
              "\n===================================")

    # Check the Crosswalk for a FHIR Id for this user

    # If no Crosswalk entry let's check to see if we have a match on
    # name, dob and addressLine1

    # Now we need to see if there is a patient record
    patient_count = match_patient(request, json_stuff)

    if settings.DEBUG:
        print("Patient Count: ", patient_count,
              "\n Request.user:", request.user)

    if patient_count > 1:
        result['reason'] = "Unable to match a patient record. We " \
                           "have multiple patient records matching. " \
                           "We found " + str(patient_count) + " records."
        messages.error(request,result['reason'])
        return result

    patient_id = x_walk.get_fhir_url_id()

    if settings.DEBUG:
        print("=====================",
              "\nWorking with Patient Id:",
              patient_id,
              "\nGUID:", guid,
              "\n===========")

    claims = json_stuff['claims']
    if settings.DEBUG:
        print("How many claims:", len(claims),
              ":", claims,
              "\n\n\n\nSection 0:", claims[0])

    if "claimNumber" in claims[0]:
        for claim in claims:
            # Deal with the Claim Header
            extension = []
            extension.append(extn_item("Patient", patient_id, "valueString"))
            extension.append(extn_item("identifier", guid, "valueString"))
            for key, value in claim.items():

                # if settings.DEBUG:
                #     print("Key:", key)
                #     print("Value:", value)

                if key == "claimNumber":
                    add_it = extn_item(key, value, "valueString",)
                    claim_number = value
                    extension.append(add_it)
                elif key == "claimType":
                    add_it = extn_item(key, value, "valueString")
                    extension.append(add_it)
                elif key == "provider":
                    add_it = extn_item(key, value, "valueString")
                    extension.append(add_it)
                elif key == "providerBillingAddress":
                    add_it = extn_item(key, value, "valueString")
                    extension.append(add_it)
                elif key == "date":
                    period = {}
                    if value['serviceStartDate']:
                        period['start'] = value['serviceStartDate']
                    if value['serviceEndDate']:
                        period['end'] = value['serviceEndDate']
                    add_it = extn_item(key, period, "valuePeriod")
                    extension.append(add_it)
                    # Set created to the Service End Date.
                    # This should be easier to track duplicate
                    # EOB entries
                    created = value['serviceEndDate']

                elif key == "diagnosisCode1":
                    add_it = extn_item(key, value, "valueString")
                    extension.append(add_it)
                elif key == "diagnosisCode2":
                    add_it = extn_item(key, value, "valueString")
                    extension.append(add_it)
                elif key == "source":
                    add_it = extn_item(key, value, "valueString")
                    extension.append(add_it)
                elif key == "charges":
                    for ckey, charge in value.items():
                        add_it = extn_item(ckey,charge, "valueString")
                        extension.append(add_it)
                elif key == "details":
                    # Deal with the Claim Lines
                    add_it = claim_detail(details=value)
                    add_it = extn_item(key,add_it,"valueString")
                    extension.append(add_it)

            eob_extn = [{"url" : "https://dev.bbonfhir.com/fhir/StructureDefinition/cms-eob",
                     "extension": extension}]

            #if settings.DEBUG:
            #    print("==================================",
            #          "extension:", eob_extn,
            #          "\n==================================")

            # Now we need to write an EOB Resource to the server.
            eob = OrderedDict()
            eob['resourceType'] = "ExplanationOfBenefit"

            id_source = {}
            id_list = []
            id_source['system'] = "https://mymedicare.gov/claims"
            id_source['use'] = "official"
            id_source['value'] = claim_number
            id_list.append(unique_id(id_source))

            id_source['system'] = "https://mymedicare.gov/claims/beneficiary"
            id_source['use'] = "official"
            id_source['value'] = "Patient/"+str(patient_id)
            id_list.append(unique_id(id_source))

            eob['identifier']   = id_list
            eob['outcome']      = "complete"
            eob['extension']    = eob_extn


            #if settings.DEBUG:
            #    print("EOB:", eob)

            txn = {'resourceType': "ExplanationOfBenefit",
                   'server': settings.FHIR_SERVER,
                   'locn': "/baseDstu2/ExplanationOfBenefit"}

            target_url = txn['server'] + txn['locn']

            # Can we write the EOB now....
            headers = {'Content-Type': 'application/json+fhir; charset=UTF-8',
                       'Accept': 'text/plain'}

            try:
                r = requests.post(target_url + "?_format=json",
                                  data=json.dumps(eob),
                                  headers=headers )
                if r.status_code == 201:
                    commit_data = r.headers['content-location']
                    if settings.DEBUG:
                        print("Write returned:", r.status_code,
                              "|", commit_data)
                elif r.status_code == 400:
                    if settings.DEBUG:
                        print(r.status_code," Problem with input")
                        print(rec_counter,":","Mode:",
                              claim_number,"[",
                              r.status_code,
                              "] NPI:",
                              row_under['NPI'],
                              r.__dict__)
            except requests.ConnectionError:
                messages.error(request,"Problem posting:" + claim_number)

            if settings.DEBUG:
                print("Result from post", r.status_code, "|",
                      r.content, "|",
                      r.text, "|",
                      "Headers", r.headers)
        result['result'] = "OK"
        result['reason'] = "Claims extracted from BlueButton file and posted as EOBs"
        messages.info(request, result['reason'])
        return result
    else:
        result['result'] = "FAIL"
        result['reason'] = "No claims found in BueButton file " + str(claims[0])
        messages.info(request, result['reason'])
        return result

    result['reason'] = "BlueButton file processed"
    messages.info(request, result['reason'])
    return result


def write_eob(request, patient_id, bbj_in):
    """

    :param request:
    :param patient_id:
    :param bbj_in:
    :return:
    """

    if settings.DEBUG:
        print("Patient_Id =", patient_id)
        print("JSON File =", bbj_in)

    demodict = cms_file_read(settings.MEDIA_ROOT+bbj_in)
    json_stuff = parse_lines(demodict)

    if settings.DEBUG:
        print("Converted BlueButton File:\n",
              json_stuff,
              "\n===================================")

    #jfn = open(settings.MEDIA_ROOT+bbj_in, 'r')
    #json_stuff = json.load(jfn)
    # print("stuff:", json_stuff)
    #jfn.close()

    # Check the Crosswalk for a FHIR Id for this user

    # If no Crosswalk entry let's check to see if we have a match on
    # name, dob and addressLine1

    # Now we need to see if there is a patient record
    patient_count = match_patient(request, json_stuff)

    if settings.DEBUG:
        print("Patient Count: ", patient_count,
              "\n Request.user:", request.user)

    if patient_count > 1:
        messages.error(request,"Unable to match a patient record. We"
                               "have multiple patient records matching."
                               " We found ", patient_count, " records.")
        return HttpResponseRedirect(reverse("eob_upload:home"))
    elif patient_count == 0:
        # We need to create a patient resource record
        # If there is no fhir_url_id in the crosswalk for request.user
        try:
            x_walk = Crosswalk.objects.get(user=request.user)
            guid = x_walk.guid
            patient_id = x_walk.get_fhir_url_id()
        except Crosswalk.DoesNotExist:
            # No Crosswalk so create a patient

            result = create_patient(request, bb_dict=json_stuff)

            # create_patient should have created a crosswalk entry
            x_walk = Crosswalk.objects.get(user=request.user)
            guid = x_walk.guid
            patient_id = x_walk.get_fhir_url_id()
    else: # patient_count == 1:
        #
        x_walk = Crosswalk.objects.get(user=request.user)
        guid = x_walk.guid
        patient_id = x_walk.get_fhir_url_id()

    if settings.DEBUG:
        print("=====================",
              "\nWorking with Patient Id:",
              patient_id,
              "\nGUID:", guid,
              "\n===========")

    claims = json_stuff['claims']

    for claim in claims:
        # Deal with the Claim Header
        extension = []
        extension.append(extn_item("Patient", patient_id, "valueString"))
        extension.append(extn_item("identifier", guid, "valueString"))
        for key, value in claim.items():

            # if settings.DEBUG:
            #     print("Key:", key)
            #     print("Value:", value)

            if key == "claimNumber":
                add_it = extn_item(key, value, "valueString",)
                claim_number = value
                extension.append(add_it)
            elif key == "claimType":
                add_it = extn_item(key, value, "valueString")
                extension.append(add_it)
            elif key == "provider":
                add_it = extn_item(key, value, "valueString")
                extension.append(add_it)
            elif key == "providerBillingAddress":
                add_it = extn_item(key, value, "valueString")
                extension.append(add_it)
            elif key == "date":
                period = {}
                if value['serviceStartDate']:
                    period['start'] = value['serviceStartDate']
                if value['serviceEndDate']:
                    period['end'] = value['serviceEndDate']
                add_it = extn_item(key, period, "valuePeriod")
                extension.append(add_it)
                # Set created to the Service End Date.
                # This should be easier to track duplicate
                # EOB entries
                created = value['serviceEndDate']

            elif key == "diagnosisCode1":
                add_it = extn_item(key, value, "valueString")
                extension.append(add_it)
            elif key == "diagnosisCode2":
                add_it = extn_item(key, value, "valueString")
                extension.append(add_it)
            elif key == "source":
                add_it = extn_item(key, value, "valueString")
                extension.append(add_it)
            elif key == "charges":
                for ckey, charge in value.items():
                    add_it = extn_item(ckey,charge, "valueString")
                    extension.append(add_it)
            elif key == "details":
                # Deal with the Claim Lines
                add_it = claim_detail(details=value)
                add_it = extn_item(key,add_it,"valueString")
                extension.append(add_it)

        eob_extn = [{"url" : "https://dev.bbonfhir.com/fhir/StructureDefinition/cms-eob",
                 "extension": extension}]

        #if settings.DEBUG:
        #    print("==================================",
        #          "extension:", eob_extn,
        #          "\n==================================")

        # Now we need to write an EOB Resource to the server.
        eob = OrderedDict()
        eob['resourceType'] = "ExplanationOfBenefit"

        id_source = {}
        id_list = []
        id_source['system'] = "https://mymedicare.gov/claims"
        id_source['use'] = "official"
        id_source['value'] = claim_number
        id_list.append(unique_id(id_source))

        id_source['system'] = "https://mymedicare.gov/claims/beneficiary"
        id_source['use'] = "official"
        id_source['value'] = "Patient/"+str(patient_id)
        id_list.append(unique_id(id_source))

        eob['identifier']   = id_list
        eob['outcome']      = "complete"
        eob['extension']    = eob_extn


        #if settings.DEBUG:
        #    print("EOB:", eob)

        txn = {'resourceType': "ExplanationOfBenefit",
               'server': settings.FHIR_SERVER,
               'locn': "/baseDstu2/ExplanationOfBenefit"}

        target_url = txn['server'] + txn['locn']

        # Can we write the EOB now....
        headers = {'Content-Type': 'application/json+fhir; charset=UTF-8',
                   'Accept': 'text/plain'}

        try:
            r = requests.post(target_url + "?_format=json",
                              data=json.dumps(eob),
                              headers=headers )
            if r.status_code == 201:
                commit_data = r.headers['content-location']
                if settings.DEBUG:
                    print("Write returned:", r.status_code,
                          "|", commit_data)
            elif r.status_code == 400:
                if settings.DEBUG:
                    print(r.status_code," Problem with input")
                    print(rec_counter,":","Mode:",
                          claim_number,"[",
                          r.status_code,
                          "] NPI:",
                          row_under['NPI'],
                          r.__dict__)
        except requests.ConnectionError:
            messages.error(request,"Problem posting:" + claim_number)

        if settings.DEBUG:
            print("Result from post", r.status_code, "|",
                  r.content, "|",
                  r.text, "|",
                  "Headers", r.headers)

    form = {}

    return render_to_response('eob_upload/eob.html',
                              {'documents': claims,
                               'patient_id': patient_id,
                               'eob': json.dumps(eob,
                                                 indent=4,
                                                 ),
                               'form': form},
                              context_instance=RequestContext(request)
                              )

"""
Claim: {
    'date': {'serviceEndDate': '20140105', 'serviceStartDate': '20140105'},
    'category': 'claim Header',
    'details': [
        {'claimNumber': '11122233310000',
         'lineNumber': '1',
         'details': 'Claim Lines for Claim Number',
         'nonCovered': '$44.55',
         'dateOfServiceFrom': '20140105',
         'modifier3Description': '',
         'modifier4Description': '',
         'renderingProviderNpi': '',
         'modifier2Description': 'KX - Requirements Specified In The Medical Policy Have Been Met',
         'renderingProviderNo': 'DMEPROVIDR',
         'category': 'Claim Lines for Claim Number',
         'allowedAmount': '$90.45',
         'typeOfServiceDescription': 'R - Rental of DME',
         'quantityBilledUnits': '1',
         'submittedAmountCharges': '$135.00',
         'modifier1Description': 'MS - Six Month Maintenance And Servicing Fee For Reasonable And Necessary Parts And Labor Which Are',
         'procedureCodeDescription': 'E0601 - Continuous Positive Airway Pressure (Cpap) Device',
         'source': 'MyMedicare.gov',
         'placeOfServiceDescription': '12 - Home',
         'dateOfServiceTo': '20140105'
        }
     ],
     'diagnosisCode2': 'E8889',
     'charges': {
        'providerPaid': '$7.50',
        'medicareApproved': '$9.38',
        'youMayBeBilled': '$1.88',
        'amountCharged': '$38.00'
        },
     'source': 'MyMedicare.gov',
     'claim': 'claim Header',
     'claimNumber': '2333444555400',
     'claimType': 'PartB',
     'providerBillingAddress': '',
     'provider': 'No Information Available',
     'diagnosisCode1': '9593'
}



{
 "resourceType" : "ExplanationOfBenefit",
 // from Resource: id, meta, implicitRules, and language
 // from DomainResource: text, contained, extension, and modifierExtension
 "identifier" : [{ Identifier }], // Business Identifier
 "contained" : [
    {"resourceType" : "Practitioner",
     "id" : "practitioner1",  // relevant patient facing information ...
    },
    {"resourceType" : "Organization",
     "id" : "org1",
       // relevant patient facing information... }
       // embed any other potentially repeating information
       // refer to item via relative link e.g. #practitioner1 from
       // elsewhere in the EOB document
       // Each item in the contains section should contain an id that enables
       // a suitably authorized person to track back to the original record.
 ],
 "request" : { Reference(ClaimResponse) }, // Claim reference and details
 "outcome" : "<code>", // complete | error
 "disposition" : "<string>", // Disposition Message
 "period" :  { Period }, // Claim start and end dates
 "adjudication" : [{ // claim adjudication
   "code" : { Coding }, // R!  Adjudication category such as co-pay, eligible, benefit, etc.
   "amount" : { Quantity(Money) }, // Monetary amount
   "value" : <decimal> // Non-monitory value
 }],
 "organization" : { Reference(Organization) },  // payer
 "coverage" :  { "identifier" : Reference(Identifier),
                 "plan" : "<string>" },
 "text" : "<string>" // text representation of EOB content
}

{

"extension" : [
    {"url" : "https://dev.bbonfhir.com/fhir/StructureDefinition/cms-eob",
     "extension" : [{ "url" : "claimNumber",
                      "valueString" : "11122233320000"},
                          {"url" : "date", 
                           "valuePeriod" : {"start" : "2014-01-05",
                                            "end": "2014-01-05"}}  
                    ]
    }]
"""


def claim_detail(details=[]):
    """
    receive a dict of claim details.
    Map the dict to FHIR EOB Claim detail
    :param details:
    :return:

         #'lineNumber': '1',
         #'details': 'Claim Lines for Claim Number',
         #'nonCovered': '$44.55',
         #'dateOfServiceFrom': '20140105',
         #'modifier3Description': '',
         #'modifier4Description': '',
         #'renderingProviderNpi': '',
         #'modifier2Description': 'KX - Requirements Specified In The Medical Policy Have Been Met',
         #'renderingProviderNo': 'DMEPROVIDR',
         #'category': 'Claim Lines for Claim Number',
         #'allowedAmount': '$90.45',
         #'typeOfServiceDescription': 'R - Rental of DME',
         #'quantityBilledUnits': '1',
         #'submittedAmountCharges': '$135.00',
         #'modifier1Description': 'MS - Six Month Maintenance And Servicing Fee For Reasonable And Necessary Parts And Labor Which Are',
         #'procedureCodeDescription': 'E0601 - Continuous Positive Airway Pressure (Cpap) Device',
         #'source': 'MyMedicare.gov',
         #'placeOfServiceDescription': '12 - Home',
         #'dateOfServiceTo': '20140105'
        }



    """
    result = []
    add_it = {}

    start = ""
    end = ""

    for detail in details:
        if len(detail) >0:
            for key, value in detail.items():
                #if settings.DEBUG:
                #    print("Details: Key:", key)
                #    print(" Detail Value:", value)
                if key == "lineNumber":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "source":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "dateOfServiceFrom":
                    start = value
                elif key == "dateOfServiceTo":
                    end = value
                elif key == "renderingProviderNpi":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "renderingProviderNo":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "typeOfServiceDescription":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "modifier1Description":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "modifier2Description":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "modifier3Description":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "modifier4Description":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "quantityBilledUnits":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "placeOfServiceDescription":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "procedureCodeDescription":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "submittedAmountCharges":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "allowedAmount":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)
                elif key == "nonCovered":
                    add_it = extn_item(key, value, "valueString")
                    result.append(add_it)

            if not start + end == "":
                add_it = extn_item("period", {'start': start,
                                              'end': end}, "valuePeriod")
        result.append(add_it)

    return result


def claim_header(header={}):
    """
    Map a Claim to a FHIR EOB

    :param header:
    :return:
    """

    result = {}

    # TODO: We need to build out the EOB definition
    if len(header) > 0:
        result = header

    return result


def contained_practitioner(claim={}):
    """
    Create a Contained Practitioner resource for the EOB

    write out a record with a relative reference

    :param claim:
    :return:
    """

    result = {}

    # TODO: We need to build out the EOB definition
    if len(claim) > 0:
        result = claim

    return result

def contained_organization(claim={}):
    """
    Create a Contained Organization resource for the EOB

    write out a record with a relative reference

    :param claim:
    :return:
    """

    result = {}

    # TODO: We need to build out the EOB definition
    if len(claim) > 0:
        result = claim

    return result


def claim_adjudication(claim={}):
    """
    Create an adjudication element for the  EOB

    Convert:
         'charges': {
        'providerPaid': '$7.50',
        'medicareApproved': '$9.38',
        'youMayBeBilled': '$1.88',
        'amountCharged': '$38.00'
        },

    To:

    "adjudication" : [{ // claim adjudication
         "code" : { Coding }, // R!  Adjudication category such as co-pay, eligible, benefit, etc.
         "amount" : { Quantity(Money) }, // Monetary amount
         "value" : <decimal> // Non-monitory value
    }],

    :param claim:
    :return:
    """

    result = {}

    # TODO: We need to build out the EOB definition
    if len(claim) > 0:
        result = claim

    return result


def extn_item(k, v , valtype):
    """
    take the item and set it as value for url field
    Identify the data type and set the value for the item to the
    value type.

    {
    // from Element: extension
    "url" : "<uri>", // R!  identifies the meaning of the extension
    // value[x]: Value of extension. One of these 23:
    "valueInteger" : <integer>
    "valueDecimal" : <decimal>
    "valueDateTime" : "<dateTime>"
    "valueDate" : "<date>"
    "valueInstant" : "<instant>"
    "valueString" : "<string>"
    "valueUri" : "<uri>"
    "valueBoolean" : <boolean>
    "valueCode" : "<code>"
    "valueBase64Binary" : "<base64Binary>"
    "valueCoding" : { Coding }
    "valueCodeableConcept" : { CodeableConcept }
    "valueAttachment" : { Attachment }
    "valueIdentifier" : { Identifier }
    "valueQuantity" : { Quantity }
    "valueRange" : { Range }
    "valuePeriod" : { Period }
    "valueRatio" : { Ratio }
    "valueHumanName" : { HumanName }
    "valueAddress" : { Address }
    "valueContactPoint" : { ContactPoint }
    "valueSchedule" : { Schedule }
    "valueReference" : { Reference }
    }

    :return: dict
    """

    result = {"url": k,
              valtype : v}

    return result


def match_patient(request, bb_dict):
    """
    Receive blueButton json dict.
    We need to see if there is a patient match on FHIR.

    Match on (Family, Given, dateOfBirth, Address)

    :param bb_dict:
    :return:
    """

    result = 0
    # Step 1: Get the fields to search with from the BlueButton dict

    person = bb_dict['patient']['name']

    names = person.split(" ")
    # We will take the last entry in names and assign as family name
    # We will take first entry and assign as given name

    given = ""
    family = ""
    if len(names) > 0:
        given = names[0]
        family = names[len(names)-1]

    dob = bb_dict['patient']['dateOfBirth'][:4]+"-"
    dob = dob + bb_dict['patient']['dateOfBirth'][5:6].rjust(2, "0")+"-"
    dob = dob + bb_dict['patient']['dateOfBirth'][7:8].rjust(2, "0")

    address_line1 = bb_dict['patient']['address']['addressLine1']

    # Step 2: Construct the search url
    SearchParameter = "family=%s&given=%s&birthdate=%s&address=%s" % (family, given, dob, address_line1)

    if settings.DEBUG:
        print("Person's name:", person)
        print("Given:", given, "| Family:", family)
        print("Date of Birth:", dob, "(", bb_dict['patient']['dateOfBirth'], ")")
        print("address:", address_line1)
        print("Search with:", SearchParameter)


    # We need to construct this url:
    # {server}
    # /baseDstu2/Patient
    # ?{searchParameter}
    # &_format=json

    # search_spec = {'namespace': "http://www.cms.gov",
    #                        'txn'  : context['txn'],
    #                        'field': "identifier",
    #                        'value': "NPI", # Field Name from Profile
    #                        }
    # txn =  {'resourceType' :"Patient",
    #        'display' :'Patient',
    #        'mask'  : True,
    #        'server': settings.FHIR_SERVER,
    #        'locn'  : "/baseDstu2/Patient",
    #        'template' : 'v1api/fhir_profile/patient',
    #        'extn'  : 'json.html',}

    txn = {'resourceType' :"Patient",
           'display' :'Patient',
           'mask'  : True,
           'server': settings.FHIR_SERVER,
           'locn'  : "/baseDstu2/Patient",
           'template' : 'v1api/fhir_profile/patient',
           'extn'  : 'json.html',}

    search_spec = {'namespace': "http://www.cms.gov",
                   'txn': txn,
                   'field': "COMPLEX_MULTI_VARIABLE",
                   'value': SearchParameter,
                  }

    search_result = find_profile(request,
                                 "Patient",
                                 bb_dict,
                                 search_spec=search_spec )
    # Step 3: check the results

    if 'total' in search_result:
        if search_result['status_code'] == 200:
            if search_result['total'] > 0:
                result = int(search_result['total'])

    if settings.DEBUG:
        print("Search Result:",
              search_result,
              "\nresult:", result)

    # Step 4: return the result

    return result


def create_patient(request, bb_dict):
    """
    Create a Patient Profile using the contents of bb_dict
    (Medicare BlueButton 2.0 Text converted to json)

    :param request:
    :param bb_dict:
    :return:
    """

    # Get a Crosswalk entry for the user and use the Guid as
    # the identifier

    try:
        x_walk = Crosswalk.objects.get(user=request.user)
    except Crosswalk.DoesNotExist:
        x_walk = Crosswalk
        x_walk.user = request.user
        x_walk.save()

    x_walk = Crosswalk.objects.get(user=request.user)
    guid = x_walk.guid

    if settings.DEBUG:
        print("CrossWalk Match:", x_walk,
              "\nGUID:", guid,
              "\nFHIR Id:",x_walk.fhir, "|", x_walk.fhir_url_id )


    # Compile Profile content

    profile = {}
    profile['resourceType'] = "Patient"
    profile['mode'] = "create"
    profile['versionId'] = "1"
    profile['updated'] = date_to_iso(datetime.datetime.now())
    profile['active'] = "True"

    id_list = []
    id_source = {}
    id_source['system'] = "https://mymedicare.gov"
    id_source['use'] = "official"
    id_source['value'] = guid

    id_list.append(unique_id(id_source))

    profile['fhir_identifier'] = id_list

    person = bb_dict['patient']['name']

    names = person.split(" ")
    # We will take the last entry in names and assign as family name
    # We will take first entry and assign as given name

    given = ""
    family = ""
    if len(names) > 0:
        profile['given'] = [names[0]]
        profile['family'] = [names[len(names)-1]]

    # Done: Fix call to human_name - breaking out to chars
    profile['fhir_human_name'] = human_name(profile)

    telecom_source = {}
    tel_list = []
    rank = 1
    telecom_source['system'] = "phone"
    telecom_source['value']  = bb_dict['patient']['phoneNumber'][0]
    telecom_source['rank']   = str(rank)

    tel_list.append(contact_point(telecom_source))
    rank += 1
    telecom_source['system'] = "email"
    telecom_source['value']  = bb_dict['patient']['email']
    telecom_source['rank']   = str(rank)

    tel_list.append(contact_point(telecom_source))

    profile['fhir_contact_point'] = tel_list

    addr_source = {}
    addr_list = []

    addr_source['use']   = "primary"
    addr_source['type']  = "physical"
    addr_source['line']  = [bb_dict['patient']['address']['addressLine1'],
                            bb_dict['patient']['address']['addressLine2']]
    addr_source['city']  = bb_dict['patient']['address']['city']
    addr_source['state'] = bb_dict['patient']['address']['state']
    addr_source['postalCode'] = bb_dict['patient']['address']['zip']

    addr_list.append(address(addr_source))

    profile['fhir_address'] = addr_list

    narrative = concat_string("", profile['given'],
                              delimiter=" ",
                              last=" ")
    narrative = concat_string(narrative, profile['family'],
                              delimiter=" ",
                              last = " ")
    narrative = concat_string(narrative, [" (id:",
                                          guid, ")"])

    narrative = concat_string(narrative, addr_source['line'],
                              delimiter=",",
                              last=",")
    narrative = concat_string(narrative, addr_source['city'],
                              last=" ")
    narrative = concat_string(narrative, addr_source['state'],
                              last=" ")
    narrative = concat_string(narrative, addr_source['postalCode']
                              )

    profile['narrative'] = narrative

    if settings.DEBUG:
        print("Profile:", profile, "\n====================")

    # Write Profile

    txn = {'resourceType' :"Patient",
           'display' :'Patient',
           'mask'  : True,
           'server': settings.FHIR_SERVER,
           'locn'  : "/baseDstu2/Patient",
           'template' : 'v1api/fhir_profile/patient',
           'extn'  : 'json.html',}

    context = {'txn': txn,
               'profile': profile,}
    fhir_profile = build_fhir_profile(request,
                                      context,
                                      context['txn']['template'],
                                      context['txn']['extn'],
                                     )

    if settings.DEBUG:
        print("===============================",
              "FHIR Profile:\n",
              fhir_profile,
              "===============================")
    # Submit to server
    target_url = context['txn']['server'] + context['txn']['locn']
    headers = {'Content-Type': 'application/json+fhir; charset=UTF-8',
               'Accept'      : 'text/plain'}

    try:
        if profile['mode'] == 'create':
            r = requests.post(target_url + "?_format=json",
                              data=fhir_profile,
                              headers=headers )
        else:
            r = requests.put(target_url + "/" + x_walk.fhir_url_id + "?_format=json",
                             data=fhir_profile,
                             headers=headers )
        r_returned = r.text

        print("Result from post", r.status_code, "|",
              r_returned, "|",
              r.content, "|",
              r.text, "|",
              "Headers", r.headers)

    except requests.ConnectionError:
        messages.error(request,"Problem posting:" + guid)

    if r.status_code == 201:
        url_result = r.headers['content-location']
        if settings.DEBUG:
            print("url_content_location", url_result)
        result = get_fhir_url(url_result, "Patient")

        if settings.DEBUG:
            print("result:", result, "|", result[1], "|")

        x_walk.fhir_url_id = result[1]
        x_walk.save()
    # Get Id from successful write
    # Update Patient Crosswalk

    return


def get_fhir_url(url, profile_name):
    """

    Get the url content-location from the header
    use the profile_name to find the section in the url we want

    http://ec2-52-4-198-86.compute-1.amazonaws.com:8080/baseDstu2/Patient/4995293/_history/1
    Profile = Patient


    :param url:
    :param profile_name:
    :return:
    """

    profile = "/%s/" % profile_name
    u_split = url.split(profile)
    profile_id = u_split[1].split("/", 1)
    result = [u_split[0], profile_id[0],profile_id[1]]
    if settings.DEBUG:
        print(url, " Split with ", profile, " to yield",
              u_split, " which is then split to ", profile_id,
              "\nbefore being reconstituted as ", result)

    return result

