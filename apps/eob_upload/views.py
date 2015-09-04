# -*- coding: utf-8 -*-
"""
bbofuser: eob_upload
FILE: views
Created: 9/3/15 12:27 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

import json

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.eob_upload.forms import BlueButtonJsonForm


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

    jfn = open(settings.MEDIA_ROOT+bbj_in, 'r')

    json_stuff = json.load(jfn)

    # print("stuff:", json_stuff)

    jfn.close()

    claims = json_stuff['claims']

    for claim in claims:
        print("====================================")
        print("Claim:", claim, "\n")

"""
Claim: {
    'date': {'serviceEndDate': '20140105', 'serviceStartDate': '20140105'},
    'category': 'claim Header',
    'details': [
        {'claimNumber': '11122233310000',
         'lineNumber': '1',
         'details': 'Claim Lines for Claim Number',
         'non-Covered': '$44.55',
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


"""

    #return

def claim_detail(details={}):
    """
    receive a dict of claim details.
    Map the dict to FHIR EOB Claim detail
    :param details:
    :return:
    """

    result = {}

    # TODO: We need to build this out
    if len(details) >0:
        result = details

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


def claim_adjudication(claim={})
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
