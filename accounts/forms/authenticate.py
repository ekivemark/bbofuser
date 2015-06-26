"""
developeraccount
FILE: authenticate
Created: 6/22/15 12:31 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'
from django import forms

class AuthenticationForm(forms.Form):
    """
    Login form
    """
    email = forms.EmailField(widget=forms.widgets.TextInput)
    password = forms.CharField(widget=forms.widgets.PasswordInput)

    class Meta:
        fields = ['email', 'password']
