"""
BBonFHIRUser
FILE: application
Created: 6/27/15 7:58 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.shortcuts import render, get_object_or_404
from django import forms
from django.conf import settings
#from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Submit

from accounts.models import Application


def application_view(request, mymodel_id):
    class MyModelForm(forms.ModelForm):
        class Meta:
            model = Application

    model = get_object_or_404(Application, pk=mymodel_id)
    form = MyModelForm(instance=model)
    return render(request, 'developer/model.html', {'form': form})


class ApplicationCheckForm(forms.Form):
    """
    A form for checking an Organization top level url
    """
    #    site_url = forms.CharField(label="Organization URL",
    #                               help_text="enter the top level organization domain. eg. domain.com")

    name = forms.CharField(label="Application Name", )
    callback = forms.URLField(label="Callback URL",
                              help_text="Enter the callback url")
    icon_link = forms.URLField(required=False,
                               label="Link to Application Icon",
                               help_text="Enter a web address where your application icon is available")

    if settings.DEBUG:
        print("in ApplicationCheckForm")

    def clean(self):

        if settings.DEBUG:
            print("checking for this:", self.cleaned_data)
        # check_for = strip_url(self.cleaned_data['domain'],"www")
        # check_for = check_for.replace("http://","")
        # check_for = check_for.replace("https://","")
        # check_for = check_for.replace("www.","")

        check_for = self.cleaned_data['name']

        if settings.DEBUG:
            print("Check_for:", check_for)

        return self.cleaned_data


class Application_Form(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['id']

        def __init__(self, *args, **kwargs):
            super(Application_Form, self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.layout.append(Submit('submit', 'Submit'))


class Application_EditForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['redirect_uris',
                  'client_type',
                  'authorization_grant_type',
                  'skip_authorization',
                  ]
