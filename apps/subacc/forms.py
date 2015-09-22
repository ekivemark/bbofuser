"""
bbofuser:device
FILE: forms
Created: 8/3/15 6:46 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django import forms
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.forms import (HiddenInput, Textarea)

from apps.subacc.models import (Device, DeviceAccessLog)
from apps.subacc.utils import LowerCaseCharField
# Form Field that converts to lower case

def unique_account(acc):
    """
    Check acc against Device for unique Account
    Return True if Acc not found
    :param acc:
    :return: True or False
    """

    result = False
    try:
        d = Device.objects.get(account=acc)
    except Device.DoesNotExist:
        d = None
        result = True

    if settings.DEBUG:
        print("Unique Account:", result, '[', d, ']', '[', acc, ']')

    return result


def Device_View(request, mymodel_id):
    class MyModelForm(forms.ModelForm):
        class Meta:
            model = Device

    model = get_object_or_404(Device, pk=mymodel_id)
    form = MyModelForm(instance=model)
    return render(request, 'subacc/model.html', {'form': form})

class Device_Form(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['id',
                  'device',
                  'account',
                  'active',]

        def __init__(self, *args, **kwargs):
            super(Device_Form, self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.layout.append(Submit('submit', 'Submit'))


class Device_EditForm(forms.ModelForm):
    # DONE: Account must be unique across all users AND Devices
    # DONE: account and password should be lower case
    device = forms.CharField(max_length=40,
                             label='Nick name',
                             help_text="Enter a Sub-account name")
    account = LowerCaseCharField(max_length=80,
                                 label='User name',
                                 help_text='Used for device login',
                              widget=forms.Textarea(attrs={'rows': 1,
                              'cols': 80}))
    password = LowerCaseCharField(max_length=40, widget=HiddenInput())
    valid_until = forms.DateTimeField()
    used = forms.BooleanField(required=False , help_text="Has Sub-account been used to connect to your account?")
    permitted = forms.BooleanField(required=False, help_text="Has permission been given for this Sub-account to access your account?")

    class Meta:
        model = Device
        fields = ('device',
                  'account',
                  'valid_until',
                  'password',
                  'active',
                  'used',
                  'permitted',
                  )
    def clean(self):
        error_messages = []

        if len(error_messages):
            raise forms.ValidationError(' & '.join(error_messages))

        return self.cleaned_data


class Device_AddForm(forms.ModelForm):
    # DONE: Account must be unique across all users AND Devices
    device = forms.CharField(max_length=40,
                             label='Sub-account Nick name',
                             help_text="Enter a Sub-account name")
    account = LowerCaseCharField(max_length=80,
                              widget=forms.Textarea(attrs={'rows': 1,
                              'cols': 80}), label='Sub-account username',
                                 help_text="Used for Sub-account Login")
    password = LowerCaseCharField(max_length=40, widget=HiddenInput())
    active = forms.BooleanField(initial=True)
    valid_until = forms.DateTimeField()

    class Meta:
        model = Device
        fields = ('device',
                  'account',
                  'valid_until',
                  'password',
                  'active',
                  )
    def clean(self):
        # Check that account is unique in subacc table
        error_messages = []
        if not unique_account(self.cleaned_data['account']):
            error_messages.append("Account: Name is not available")

        if len(error_messages):
            raise forms.ValidationError(' & '.join(error_messages))

        return self.cleaned_data


# DONE: Create Device Authentication Form for Subaccount_Login View
class Device_AuthenticationForm(forms.Form):
    """
    Device Login form
    """
    account = LowerCaseCharField(widget=forms.widgets.TextInput)
    password = LowerCaseCharField(widget=forms.widgets.PasswordInput,
                                  label="Key")

    class Meta:
        fields = ['account',
                  'password', ]


class DeviceAccessLog_Form(forms.ModelForm):
    """
    Form for Device Access Log
    """

    account     = forms.CharField(max_length=80)
    action      = forms.CharField(max_length=10)
    info        = forms.CharField(max_length=200, required=False )
    source      = forms.CharField(max_length=50, required=False)

    class Meta:
        model = DeviceAccessLog
        fields = (
            'device',
            'account',
            'action',
            'info',
            'source'
        )


class Question_Form(forms.Form):
    """
    Ask Secret Question
    """
    answer = forms.CharField(max_length=80, )
    question = forms.CharField(max_length=80, widget=forms.HiddenInput())
