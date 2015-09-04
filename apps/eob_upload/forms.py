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
    bbjfile = forms.FileField(label="Select a JSON File",
                              help_text="Convert BlueButton Text to JSON "
                                        "first"
                              )

