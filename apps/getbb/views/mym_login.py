"""
bbofuser: getbb
FILE: mym_login
Created: 8/25/15 2:48 PM

Experimental app to use BeautifulSoup to attempt to login to MyMedicare.gov

"""
__author__ = 'Mark Scrimshire:@ekivemark'

import re
import requests
import urllib

from bs4 import BeautifulSoup

from robobrowser import RoboBrowser

from django.conf import settings
from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template import RequestContext

from apps.getbb.utils import *


def disconnect(request):

    return


def connect(request):
    """
    Testing Login to MyMedicare.gov
    :param request:
    :return:
    """

    PARSER = settings.BS_PARSER
    if not PARSER:
        if settings.DEBUG:
            print('Default Parser for BeautifulSoup:', 'lxml')
        PARSER = 'lxml'


    login_url = 'https://www.mymedicare.gov/default.aspx'
    username = 'MBPUSER201A'
    password = 'CMSPWD2USE'

    # soup = BeautifulSoup(login_url, PARSER )

    rb = RoboBrowser()
    rb.open(login_url)
    form = rb.get_form()

    print("Page:", rb)
    print("Form:", form)

    pwd_fld = "ctl00_ContentPlaceHolder1_ctl00_HomePage_SWEPassword"
    pwd_usr = "ctl00_ContentPlaceHolder1_ctl00_HomePage_SWEUserName"

#    <input type="button"
#           name="ctl00$ContentPlaceHolder1$ctl00$HomePage$SignIn"
#           value="Sign In"
#           onclick="ConfirmationPopup(this);__doPostBack('ctl00$ContentPlaceHolder1$ctl00$HomePage$SignIn','')"
#           id="ctl00_ContentPlaceHolder1_ctl00_HomePage_SignIn"
#           title="Sign into MyMedicare.gov"
#           class="MyMedSignInButton">


    form[pwd_usr].value = username
    form[pwd_fld].value = password


    __EVENTTARGET   = ""
    __EVENTARGUMENT = ""
    __VIEWSTATE     = VIEWSTATE

    rb.submit_form(form)

    print("RB:", rb)


    browser = RoboBrowser(history=True)
    # This gets all the ASPX stuff, __VIEWSTATE and friends
    browser.open(login_url)

    signin = browser.get_form(id='aspnetForm')

    soup = BeautifulSoup(signin, PARSER)
    print("Soup: ",soup.prettify())

    # print(browser)

    #

    formData = {
                '__VIEWSTATE': VIEWSTATE,
                '__VIEWSTATEENCRYPTED' :'' ,
                pwd_usr : username ,
                pwd_fld : password,
                'Button1': 'Show',
    }

    # print(signin)
    # signin["jsCheck"].value = ''
    #signin["ddlEngine"].value = "www.mymedicare.gov:13008"
    #signin[pwd_usr].value = username
    #signin[pwd_fld].value = password
    #signin["btnLogin.x"].value = "42"
    #signin["btnLogin.y"].value = "9"
    #signin["btnLogin"].value = "Login"
    browser.submit_form(formData)


    context = {'site' : Site.objects.get_current(),
              }
    return render_to_response('getbb/index.html',
                              RequestContext(request, context, ))
