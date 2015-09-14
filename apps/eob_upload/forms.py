# -*- coding: utf-8 -*-
"""
bbofuser eob_upload
FILE: forms
Created: 9/3/15 1:56 PM

Form for Json file upload

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django import forms

class BlueButtonJsonForm(forms.Form):
    bbjfile = forms.FileField(label="Select your CMS BlueButton 2.0 Text File",
                              help_text="You should download the text file from "
                                        "MyMedicare.gov"
                              )

