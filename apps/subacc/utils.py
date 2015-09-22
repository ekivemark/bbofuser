"""
bbofuser:device
FILE: utils
Created: 8/3/15 6:00 PM

"""
__author__ = 'Mark Scrimshire:@ekivemark'

import random

from django import forms

from django.conf import settings


def get_phrase(count=2):
    # Build a phrase
    f = open(settings.WORD_LIST)

    sentence = [x.strip() for x in f.readlines()]
    if settings.DEBUG:
        print("Sentence:", sentence)

    words = []

    for line in sentence:
        word = line.split(' ')
        if word != "":
            words += word

    if settings.DEBUG:
        print("Words:", words)

    phrase = '-'.join(random.choice(words) for i in range(count)).lower()
    phrase = phrase.replace("'", "")
    phrase = phrase + str(random.randint(1, 9999))

    if settings.DEBUG:
        print(count, "word phrase:", phrase)
    return phrase


class LowerCaseCharField(forms.CharField):
    #Create custom form field to force lower case
    def to_python(self, value):
        return value.lower()


def session_device(request, var, Session="auth_device"):
    """
    Set a Session variable if logging in via a subacc
    This will be linked to a decorator to control access to
    sections of the site that will require the master account to be used
    :param request:
    :param sessn: default is auth_device
    :param var: this should be the var to add to the session
    :return:
    """
    if not var:
        return None
    if Session == "auth_device":
        request.session['auth_device'] = var
    else:
        request.session[Session] = var
    return "%s:%s" % (Session,var)


def via_device(request):
    """
    Get Auth_device Variable
    :param request:
    :return:
    """

    if request.session["auth_device"]:
        auth_dev = request.session["auth_device"]
    else:
        auth_dev = "Master Account"

    return auth_dev


def Master_Account(request):
    """
    Check if Master Account by looking for
    :return: True or False
    """

    if request.session["auth_master"]:
            if settings.DEBUG:
                print("Not Master Account:", request.session["auth_device"])
            return False

    return True

def Device_Set_To_Permitted(device):
    """
    Set Device to Permitted
    :param device:
    :return:
    """

    device.permitted = True
    device.save()

    return device.permitted