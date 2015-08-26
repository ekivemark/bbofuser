"""
bbofuser
FILE: utils
Created: 8/17/15 11:44 AM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

import json
import time

from lxml import etree

from collections import (OrderedDict,
                         defaultdict)
from datetime import datetime

from django.conf import settings
from django.template import RequestContext
from django.template.loader import render_to_string

FORMAT_OPTIONS = ['json', 'xml']


def get_to_lower(in_get):
    """
    Force the GET parameter keys to lower case
    :param in_get:
    :return:
    """

    if not in_get:
        if settings.DEBUG:
            print("get_to_lower: Nothing to process")
        return in_get

    got_get = OrderedDict()
    # Deal with capitalization in request.GET.
    # force to lower
    for value in in_get:

        got_get[value.lower()] = in_get.get(value,"")
        if settings.DEBUG:
            print("Got key", value.lower(), ":", got_get[value.lower()] )

    if settings.DEBUG:
        print("Returning lowercase request.GET", got_get)

    return got_get


def get_format(in_get):
    """
    Receive request.GET and check for _format
    if json or xml return .lower()
    if none return "json"
    :param in_get:
    :return: "json" or "xml"
    """
    got_get = get_to_lower(in_get)

    # set default to return
    result = ""

    if "_format" in got_get:
        # we have something to process

        if settings.DEBUG:
            print("In Get:",in_get)
        fmt = got_get.get('_format','').lower()

        if settings.DEBUG:
            print("Format Returned:", fmt)

        # Check for a valid lower case value
        if fmt in FORMAT_OPTIONS:
            result = fmt
        else:
            if settings.DEBUG:
                print("No Match with Format Options:", fmt)

    return result


def xml_str_to_json_str(xmls_input, jsons_output):
    """
    Converts an xml string to json.
    """
    json_return = dict_to_json_str(etree_to_dict(xmls_to_etree(xmls_input),
                                                 True),
                                   jsons_output)
    return json_return

def xml_to_json(xml_input, json_output):
    """
    Converts an xml file to json.
    """
    dict_to_json(etree_to_dict(xml_to_etree(xml_input),
                               True),
                 json_output)
    return

def dict_to_json_str(dictionary, jsons_output):
    """
    Converts a dictionary to a json string
    :param dictionary:
    :param jsons_output:
    :return:
    """
    jsons_output = json.dumps(dictionary,
                              sort_keys=True,
                              indent=4)
    return jsons_output

def xmls_to_etree(xml_input):
    """Converts xml to a lxml etree."""
    return etree.HTML(xml_input)

def xml_to_etree(xml_input):
    """Converts xml to a lxml etree."""
    f = open(xml_input, 'r')
    xml = f.read()
    f.close()
    return etree.HTML(xml)

def etree_to_dict(tree, only_child):
    """Converts an lxml etree into a dictionary."""

    mydict = dict([(item[0], item[1]) for item in tree.items()])
    children = tree.getchildren()
    if children:
        if len(children) > 1:
            mydict['children'] = [etree_to_dict(child,
                                                False) for child in children]
        else:
            child = children[0]
            mydict[child.tag] = etree_to_dict(child,
                                              True)
    if only_child:
        return mydict
    else:
        return {tree.tag: mydict}

def dict_to_json(dictionary, json_output):
    """
    Converts a dictionary into a json file.
    :param dictionary:
    :param json_output:
    :return:
    """
    f = open(json_output,
             'w')
    f.write(json.dumps(dictionary,
                       sort_keys=True,
                       indent=4))
    f.close()
    return

def build_fhir_profile(request,context={},
                       template="",
                       extn="json.html",
                       ):
    """
    Build a FHIR Profile in JSON
    Use to submit to FHIR Server
    :param template:
    :param extn: json.html or json.xml (use .html to enable
                    template editing error checking
            (this becomes the file extension for the template)
            sms is a brief template suitable for SMS Text Messages
    :param email:
    :return:
    """
    # Template files use the Django Template System.

    this_context = {}
    if context is not None:
        # print("BMT:Context is:", context)
        this_context = RequestContext(request, context)
        # print("BMT:this_context with context:", this_context)

    if request is not None:
        # print("BMT:Request is:", request)
        this_context = RequestContext(request, this_context)

    if template=="":
        template="v1api/fhir_profile/practitioner"

    source_plate = template + "." + extn

    profile = render_to_string(source_plate, this_context)
    #if settings.DEBUG:
    #    print("Profile:",profile)

    return profile


def date_to_iso(thedate, decimals=True):
    """
    Convert date to isoformat time
    :param thedate:
    :return:
    """

    strdate = thedate.strftime("%Y-%m-%dT%H:%M:%S")

    minute = (time.localtime().tm_gmtoff / 60) % 60
    hour = ((time.localtime().tm_gmtoff / 60) - minute) / 60
    utcoffset = "%.2d%.2d" %(hour, minute)

    if decimals:
        three_digits = "."+ str(thedate.microsecond)[:3]
    else:
        three_digits = ""

    if utcoffset[0] != '-':
        utcoffset = '+' + utcoffset

    return strdate + three_digits + utcoffset

