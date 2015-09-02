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

    Name, Input, Value,
    Search_TextBox, Search_TextBox
    __EVENTARGUMENT, __EVENTARGUMENT
    __EVENTTARGET, __EVENTTARGET, ctl00$ContentPlaceHolder1$ctl00$HomePage$SignOut
    __EVENTVALIDATION, __EVENTVALIDATION, /wEWBgKEgaG9BALXoa6+DALH7qC6AQL76Z2kCwL3zdT2DALk94LQAndrVxjeqzdGXnwUEBM4LAz9UKa/$
    __VIEWSTATE, __VIEWSTATE, wEPDwUENTM4MQ9kFgJmD2QWAgIBD2QWAgIDDxYCHgZhY3Rpb24FDS9kZWZhdWx0LmFzcHgWCgIBDxUB
    __VIEWSTATEGENERATOR, __VIEWSTATEGENERATOR, CA0B0334
    __VIEWSTATEGENERATOR, __VIEWSTATEGENERATOR, 11258E27

    LAWEB_FORM_ACTION
    ctl00$ContentPlaceHolder1$ctl00$HomePage$Agree, ctl00$ContentPlaceHolder1$ctl00$HomePage$Agree, False
    ctl00$ContentPlaceHolder1$ctl00$HomePage$SignOut, * OrNew To MyMedicare.gov?
    ctl00$ContentPlaceHolder1$ctl00$HomePage$confirmString, ctl00$ContentPlaceHolder1$ctl00$HomePage$confirmString
    ctl00$ContentPlaceHolder1$ctl00$HomePage$isError, ctl00$ContentPlaceHolder1$ctl00$HomePage$isError, False
    ctl00$ContentPlaceHolder1$ctl00$HomePage$lnkCreateAccount, New To MyMedicare.gov? * Blue Button

    guid: 97290573-7965-11DF-93F2-0800200C9A66

    Search_TextBox, Search Medicare.gov * type search term here
    ctl00$ContentPlaceHolder1$ctl00$HomePage$SWEUserName, Username * -Password
    ctl00$ContentPlaceHolder1$ctl00$HomePage$SWEPassword, Password * Trouble Signing In?
    ctl00$ContentPlaceHolder1$ctl00$HomePage$SignIn, Password * Trouble Signing In?
    ctl00$ContentPlaceHolder1$ctl00$HomePage$lnkCreateAccount, New To MyMedicare.gov? * Blue Button

<input name="ctl00$ContentPlaceHolder1$ctl00$HomePage$SWEUserName" type="text"
id="ctl00_ContentPlaceHolder1_ctl00_HomePage_SWEUserName" class=" sp_clicked"
style="cursor: crosshair; ">

<input name="ctl00$ContentPlaceHolder1$ctl00$HomePage$SWEPassword"
type="password" id="ctl00_ContentPlaceHolder1_ctl00_HomePage_SWEPassword"
class=" sp_clicked">

<input type="button" name="ctl00$ContentPlaceHolder1$ctl00$HomePage$SignIn"
value="Sign In"
onclick="ConfirmationPopup(this);__doPostBack('ctl00$ContentPlaceHolder1$ctl00$HomePage$SignIn','')"
id="ctl00_ContentPlaceHolder1_ctl00_HomePage_SignIn"
title="Sign into MyMedicare.gov" class="MyMedSignInButton sp_clicked">

//form[@id='formMyMedicare']//
label[text()='By checking this box, you agree that you have read and understand the “Protecting Your Personal Health Information” section shown above and wish to continue.']


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

    if settings.DEBUG:
        print("Page:", rb)
        print("Form:", form)

    pwd_fld = "ctl00$ContentPlaceHolder1$ctl00$HomePage$SWEPassword"
    pwd_usr = "ctl00$ContentPlaceHolder1$ctl00$HomePage$SWEUserName"
    # ctl00$ContentPlaceHolder1$ctl00$HomePage$SWEUserName
    # ctl00$ContentPlaceHolder1$ctl00$HomePage$SWEPassword

#    <input type="button"
#           name="ctl00$ContentPlaceHolder1$ctl00$HomePage$SignIn"
#           value="Sign In"
#           onclick="ConfirmationPopup(this);__doPostBack('ctl00$ContentPlaceHolder1$ctl00$HomePage$SignIn','')"
#           id="ctl00_ContentPlaceHolder1_ctl00_HomePage_SignIn"
#           title="Sign into MyMedicare.gov"
#           class="MyMedSignInButton">


    form[pwd_usr].value = username
    form[pwd_fld].value = password


    EVENTTARGET   = "ctl00$ContentPlaceHolder1$ctl00$HomePage$SignIn"
    __EVENTARGUMENT = ""
    __VIEWSTATE     = VIEWSTATE

    rb.submit_form(form)

    if settings.DEBUG:
        print("RB:", rb)

    browser = RoboBrowser(history=True)
    # This gets all the ASPX stuff, __VIEWSTATE and friends
    browser.open(login_url)

    signin = browser.get_form(id='aspnetForm')

    #soup = BeautifulSoup(signin, PARSER)
    #print("Soup: ",soup.prettify())

    if settings.DEBUG:
        print("Browser:", browser)
        print("State:", rb.RoboState)

    formData = {
                '__VIEWSTATE': VIEWSTATE,
                '__EVENTTARGET':	EVENTTARGET,
                #'__VIEWSTATEENCRYPTED' :'' ,
                pwd_usr : username ,
                pwd_fld : password,
                'ctl00$ContentPlaceHolder1$ctl00$HomePage$SignIn' : "Sign In",
                #'Button1': 'ctl00$ContentPlaceHolder1$ctl00$HomePage$SignIn.MyMedSigninButton',
    }

    # print(signin)
    # signin["jsCheck"].value = ''
    #signin["ddlEngine"].value = "www.mymedicare.gov:13008"
    signin[pwd_usr].value = username
    signin[pwd_fld].value = password
    #signin["btnLogin.x"].value = "42"
    #signin["btnLogin.y"].value = "9"
    #signin["btnLogin"].value = "Login"
    #browser.submit_form(formData)

    context = {'site' : Site.objects.get_current(),
              }

    si = RoboBrowser()
    if settings.DEBUG:
        print("RB post sign-in:", rb)
        print("Sign-in:",si)

    return render_to_response('getbb/index.html',
                              RequestContext(request, context, ))
