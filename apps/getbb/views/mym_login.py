#!/usr/bin/env python
"""
bbofuser: getbb
FILE: mym_login
Created: 8/25/15 2:48 PM

Experimental app to use BeautifulSoup to attempt to login to MyMedicare.gov

"""
__author__ = 'Mark Scrimshire:@ekivemark'

import argparse
import mechanicalsoup

import re
import requests
import string
import urllib
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup

from robobrowser import (RoboBrowser,
                         browser)

from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.getbb.utils import *


def disconnect(request):

    # https://www.mymedicare.gov/signout.aspx
    context = {}

    return render_to_response('getbb/index.html',
                              RequestContext(request, context, ))


def connect(request):
    """
    Login to MyMedicare.gov using RoboBrowser
    :param request:
    :return:

    """

    PARSER = settings.BS_PARSER
    if not PARSER:
        if settings.DEBUG:
            print('Default Parser for BeautifulSoup:', 'lxml')
        PARSER = 'lxml'

    BeautifulSoup("", PARSER)

    # page = MyMedicareLoginScraper()
    # if settings.DEBUG:
    #     print("Page:", page)

    login_url = 'https://www.mymedicare.gov/default.aspx'
    username = 'MBPUSER201A'
    password = 'CMSPWD2USE'

    # Call the default page
    # We will then want to get the Viewstate and eventvalidation entries
    # we need to submit them with the form
    rb = RoboBrowser()
    rb.open(login_url)

    form = rb.get_form()

    if settings.DEBUG:
        print("Page:", rb)

    pwd_fld = "ctl00$ContentPlaceHolder1$ctl00$HomePage$SWEPassword"
    pwd_usr = "ctl00$ContentPlaceHolder1$ctl00$HomePage$SWEUserName"
    agrees = "ctl00$ContentPlaceHolder1$ctl00$HomePage$Agree"
    sign_in = "ctl00$ContentPlaceHolder1$ctl00$HomePage$SignIn"

    # if settings.DEBUG:
    #     print("Form Fields: ", form.fields)
    #     for fld in form.fields.items():
    #         if "__VIEWSTATE" in fld:
    #             print("key:", fld, "|",fld[1]._value[:120], "...Truncated." )
    #         else:
    #             print("key:", fld, "|", fld[1]._value)

    EVENTTARGET = "ctl00$ContentPlaceHolder1$ctl00$HomePage$SignIn"
    create_account = "ctl00$ContentPlaceHolder1$ctl00$HomePage$lnkCreateAccount"

    form.fields[pwd_usr].value = username
    form.fields[pwd_fld].value = password
    form.fields[agrees].value = "True"
    form.fields.pop(create_account)

    VIEWSTATEGENERATOR = form.fields['__VIEWSTATEGENERATOR']._value
    EVENTVALIDATION = form.fields['__EVENTVALIDATION']._value
    VIEWSTATE = form.fields['__VIEWSTATE']._value

    if settings.DEBUG:
        print("EventValidation:", EVENTVALIDATION )
        print("ViewStateGenerator:", VIEWSTATEGENERATOR)

    form.fields['__VIEWSTATEGENERATOR'].value = VIEWSTATEGENERATOR
    form.fields['__VIEWSTATE'].value = VIEWSTATE
    form.fields['__EVENTVALIDATION'].value = EVENTVALIDATION

    form.serialize()

    print("serialized form:", form)

    rb.submit_form(form)

    # if settings.DEBUG:
    #     print("RB:", rb)
    #     print("RB:", rb.__str__())

    browser = RoboBrowser(history=True)
    browser.parser = PARSER

    if settings.DEBUG:
        print("Browser History:", browser.history,
              "\nBrowser parser:", browser.parser,
              "\nPage html:", rb.parsed)

    context = {'site' : Site.objects.get_current(),}

    if settings.DEBUG:
        print("RB post sign-in:", rb)

    return render_to_response('getbb/index.html',
                              RequestContext(request, context, ))

