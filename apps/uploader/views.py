"""
bbofuser.uploader
FILE: views.py
Created: 7/20/15 9:51 PM


"""
from collections import OrderedDict
from datetime import datetime
from datetime import datetime

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string


__author__ = 'Mark Scrimshire:@ekivemark'
import fileinput
from collections import OrderedDict

# Date Format uses %Y %m %d identifiers
# Num format used {:nn.nf} format. Where :nn indicates the number of digits
# to left of decimal point and .n indicates decimal places.
# eg. 987654.98 would arrive as a str "98765498
# format field fmt would defined as "{:6.2f}"
# str_to_num function receives the string value and the format string
# returns a float using the 6.2f format

# DONE: Add fmt field for date and num types
PT_D_XTRCT = OrderedDict()
PT_D_XTRCT[0] = {'len': 40, 'type': "str", 'field': 'claim_cntl_num', }
PT_D_XTRCT[1] = {'len': 20, 'type': "str", 'field': 'hicn', }
PT_D_XTRCT[2] = {'len': 20, 'type': "str", 'field': 'cardholder_id', }
PT_D_XTRCT[3] = {'len': 8, 'type': "date", 'field': 'patient_dob',
                 'fmt': "%Y%m%d", }
PT_D_XTRCT[4] = {'len': 1, 'type': "str", 'field': 'gender_code', }
PT_D_XTRCT[5] = {'len': 8, 'type': "date", 'field': 'date_of_service',
                 'fmt': "%Y%m%d", }
PT_D_XTRCT[6] = {'len': 8, 'type': "date", 'field': 'paid_date',
                 'fmt': "%Y%m%d", }
PT_D_XTRCT[7] = {'len': 12, 'type': "num", 'field': 'claim_ln_svc_ref_num',
                 'fmt': "{:12.0f}"}
PT_D_XTRCT[8] = {'len': 19, 'type': 'str', 'field': 'product_svc_id', }
PT_D_XTRCT[9] = {'len': 2, 'type': "str",
                 'field': 'provider_id_qualifier', }
PT_D_XTRCT[10] = {'len': 15, 'type': "str", 'field': 'svc_provider_id', }
PT_D_XTRCT[11] = {'len': 2, 'type': 'num', 'field': 'line_rx_fill_num',
                  'fmt': "{:2.0f}"}
PT_D_XTRCT[12] = {'len': 1, 'type': "str", 'field': 'dispensing_status', }
PT_D_XTRCT[13] = {'len': 1, 'type': "num", 'field': 'compound_code',
                  'fmt': "{:1.0f}"}
PT_D_XTRCT[14] = {'len': 1, 'type': "str",
                  'field': 'product_selection_code', }
PT_D_XTRCT[15] = {'len': 10, 'type': "num", 'field': 'qty_dispensed',
                  'fmt': "{:7.3f}", }
PT_D_XTRCT[16] = {'len': 3, 'type': "num", 'field': 'days_supply',
                  'fmt': "{:3.0f}"}
PT_D_XTRCT[17] = {'len': 2, 'type': "str",
                  'field': 'prescriber_id_qualifier', }
PT_D_XTRCT[18] = {'len': 15, 'type': "str", 'field': 'prescriber_id', }
PT_D_XTRCT[19] = {'len': 1, 'type': "str",
                  'field': 'drug_coverage_status_code', }
PT_D_XTRCT[20] = {'len': 1, 'type': "str",
                  'field': 'adjustment_del_code', }
PT_D_XTRCT[21] = {'len': 1, 'type': "str",
                  'field': 'non_std_format_code', }
PT_D_XTRCT[22] = {'len': 1, 'type': "str",
                  'field': 'pricing_exception_code', }
PT_D_XTRCT[23] = {'len': 1, 'type': "str",
                  'field': 'catastrophic_coverage_ind_code', }
PT_D_XTRCT[24] = {'len': 8, 'type': "num",
                  'field': 'ingredient_cost_amount', 'fmt': "{:6.2f}", }
PT_D_XTRCT[25] = {'len': 8, 'type': "num", 'field': 'line_svc_cost_amount',
                  'fmt': "{:6.2f}", }
PT_D_XTRCT[26] = {'len': 8, 'type': "num",
                  'field': 'line_sales_tax_amount', 'fmt': "{:6.2f}", }
PT_D_XTRCT[27] = {'len': 8, 'type': "num",
                  'field': 'line_grs_below_threshold_amount',
                  'fmt': "{:6.2f}", }
PT_D_XTRCT[28] = {'len': 8, 'type': "num",
                  'field': 'line_grs_above_threshold_amount',
                  'fmt': "{:6.2f}", }
PT_D_XTRCT[29] = {'len': 8, 'type': "num",
                  'field': 'line_bene_payment_amount', 'fmt': "{:6.2f}", }
PT_D_XTRCT[30] = {'len': 8, 'type': "num",
                  'field': 'line_other_tp_paid_amount', 'fmt': "{:6.2f}", }
PT_D_XTRCT[31] = {'len': 8, 'type': "num", 'field': 'line_lis_amount',
                  'fmt': "{:6.2f}", }
PT_D_XTRCT[32] = {'len': 8, 'type': "num", 'field': 'line_plro_amount',
                  'fmt': "{:6.2f}", }
PT_D_XTRCT[33] = {'len': 8, 'type': "num",
                  'field': 'line_covered_paid_amount', 'fmt': "{:6.2f}", }
PT_D_XTRCT[34] = {'len': 8, 'type': "num",
                  'field': 'line_non_covered_paid_amount',
                  'fmt': "{:6.2f}", }
PT_D_XTRCT[35] = {'len': 5, 'type': "str",
                  'field': 'line_contract_number', }
PT_D_XTRCT[36] = {'len': 3, 'type': "str", 'field': 'pbp_id', }
PT_D_XTRCT[37] = {'len': 9, 'type': "num", 'field': 'package_id',
                  'fmt': "{:9.0f}", }
PT_D_XTRCT[38] = {'len': 102, 'type': "str", 'field': 'filler', }

# if settings.DEBUG:
#    print("Part D Extract Definition")
#    print(PT_D_XTRCT)


PT_D_DRUG_XTRCT = OrderedDict()
PT_D_DRUG_XTRCT[0] = {'len': 11, 'type': "str", 'field': 'ndc_code', }
PT_D_DRUG_XTRCT[1] = {'len': 100, 'type': "str", 'field': 'product_name', }
PT_D_DRUG_XTRCT[2] = {'len': 30, 'type': "str", 'field': 'brand_name', }
PT_D_DRUG_XTRCT[3] = {'len': 10, 'type': "str",
                      'field': 'drug_obsolete_dt', }
PT_D_DRUG_XTRCT[4] = {'len': 40, 'type': "str", 'field': 'ahfs_desc', }
PT_D_DRUG_XTRCT[5] = {'len': 1, 'type': "str", 'field': 'drug_form_code', }
PT_D_DRUG_XTRCT[6] = {'len': 1, 'type': "str",
                      'field': 'brand_name_code', }
PT_D_DRUG_XTRCT[7] = {'len': 12, 'type': "num",
                      'field': 'package_size_amount', 'fmt': "{:9.3f}", }
PT_D_DRUG_XTRCT[8] = {'len': 195, 'type': "str", 'field': 'filler', }

"""
# PROD_NDC_CD	X(11).
# PROD_NDC_PROD_NAME	X(100).
# PROD_NDC_BRAND_NAME	X(30).
# PROD_NDC_DRUG_OBSLT_DT	X(10).
# PROD_NDC_AHFS_DESC	X(40).
# PROD_NDC_DRUG_FORM_CD	X(01).
# NDC_BRND_NAME_CD	X(01).
# PROD_NDC_PKG_SIZE_AMT	9(9)V9(3).
# FILLER	X(195).
"""

@staff_member_required
def home_index(request):
    # Show UploaderHome Page


    if settings.DEBUG:
        print(settings.APPLICATION_TITLE, "in uploader.views.home_index")

    context = {}
    return render_to_response('upload.html',
                              RequestContext(request, context, ))


def str_to_num(strn, fmt):
    """
    :param s:
    :param fmt:  "{:6.2f}" ie. 65432198 becomes 654321.98
    :return: ss
    Convert String to number and insert decimal point
    """

    num_fmt = fmt[2:-2]

    digits = int(float(num_fmt))
    decimals = int((float(num_fmt) - digits) * 10)
    if settings.DEBUG:
        print("Format", fmt, "[", num_fmt, "]")
        print("digits:", digits)
        print("decimals:", decimals)

    ss = ""
    ctr = 1
    for s in strn:
        ss = ss + s
        if ctr == digits:
            ss = ss + "."
        ctr += 1

    result = float(ss)
    return result


@staff_member_required
def upload_part_d_weekly(request,
                         file_name="/Users/mark/PycharmProjects/bbofu/bbofuser/sitestatic/week_extract.txt",
                         chunkSize=400):
    """
    receive file_name as reference
    Open file

    read line

    split line to fields

    post fields to url to load to fhir server

    :param file_name:
    :return: result
    """
    # TODO: get file from upload directory - passed as parameter
    # DONE: limit access to function to staff account(s)

    if settings.DEBUG:
        print("Processing Part D Weekly Extract")
        print("file:", file_name)

    messages.info(request, "Processing lines from Part D weekly Extract")
    counter = 0
    for line in fileinput.input([file_name]):
        process_line(line, PT_D_XTRCT)
        counter +=1

    messages.info(request, str(counter) + " line(s) processed in file:" + file_name)
    # TODO: test for error in return
    # TODO: post to FHIR API

    return HttpResponseRedirect(reverse("upload:home"))


@staff_member_required
def upload_drug_extract(request,
                        file_name="/Users/mark/PycharmProjects/bbofu/bbofuser/sitestatic/week_drug_extract.txt",
                        chunkSize=400):
    """
    receive file_name as reference
    Open file

    read line

    split line to fields

    post fields to url to load to fhir server

    :param file_name:
    :return: result
    """
    # TODO: get file from upload directory - passed as parameter
    # TODO: limit access to function to special upload account(s)

    fhir_post = settings.FHIR_SERVER
    fhir_resource = "/Medications"

    if settings.DEBUG:
        print("Processing Drug Extract")
        print("file:", file_name)

    xml_upload = {}
    for line in fileinput.input([file_name]):
        m = process_line(line, PT_D_DRUG_XTRCT)

        if 'brand_name' in m:
            is_brand = "true"
        else:
            is_brand = "false"

        context = {'m': m,
                   'is_brand': is_brand}

        # DONE: Create template and merge data for line item
        xml_upload = render_to_string('uploader/medication.format.xml',
                                      context)

    if settings.DEBUG:
        print(xml_upload)

    # TODO: test for error in return
    # TODO: post to FHIR API

    return xml_upload


def process_line(file_line, format_dict):
    """
    :param file_line:
    :param format_dict:
    :return: processing result
    """

    # DONE: Added format string support
    offset_start = 0
    offset_end = 0

    result = OrderedDict()
    for k, v in format_dict.items():

        if v['len'] > 1:
            offset_end = offset_start + v['len']
        else:
            offset_end = offset_start + 1

        print(k, ":", v['field'], "type:", v['type'], " ", end="")
        s = str(file_line)[offset_start:offset_end]

        if v['type'].lower() == "date":
            # Deal with Date Formats
            if v['fmt']:
                fmt = v['fmt']
            else:
                fmt = "%Y %m %d"
            # dt = to_datetime(year=int(s[0:4]), month=int(s[4:6]), day=int(s[6:8]))
            dt = ""
            dt = datetime.strptime(s, fmt)
            print(dt)
            result[v['field']] = dt

        elif v['type'].lower() == "num":
            # Deal with Number Formats
            if v['fmt']:
                fmt = v['fmt']
            else:
                fmt = "{:%s.0f}" % len(s)

            num = str_to_num(s, fmt)
            print("Number", num)

            result[v['field']] = num

        else:
            print(s)
            result[v['field']] = s

        print("from ",
              offset_start, " to ",
              offset_end, "\n")
        if v['len'] > 1:
            offset_start = offset_end
        else:
            offset_start = offset_start + 1
            offset_end = offset_start

            # DONE: Build dictionary to return

    print(result)

    return result
