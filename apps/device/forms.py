"""
bbofuser:device
FILE: forms
Created: 8/3/15 6:46 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.shortcuts import render, get_object_or_404
from django import forms
from django.forms import (HiddenInput, Textarea)

from apps.device.models import Device


def Device_View(request, mymodel_id):
    class MyModelForm(forms.ModelForm):
        class Meta:
            model = Device

    model = get_object_or_404(Device, pk=mymodel_id)
    form = MyModelForm(instance=model)
    return render(request, 'device/model.html', {'form': form})

class Device_Form(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['id',
                  'device',
                  'account']

        def __init__(self, *args, **kwargs):
            super(Device_Form, self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.layout.append(Submit('submit', 'Submit'))


class Device_EditForm(forms.ModelForm):
    device = forms.CharField(max_length=40, help_text="Enter a device name")
    account = forms.CharField(max_length=250,
                              widget=forms.Textarea(attrs={'rows': 2,
                              'cols': 80}))
    password = forms.CharField(max_length=40, widget=HiddenInput())
    valid_until = forms.DateTimeField()

    class Meta:
        model = Device
        fields = ('device',
                  'account',
                  'valid_until',
                  'password',
                  )
