"""
developeraccount
FILE: user
Created: 7/6/15 10:16 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django import forms
from django.core import validators

from accounts.models import User

class User_EditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'mobile',
                  'carrier',
                  'affiliated_to',
                  'organization_role',
                  'mfa', ]
