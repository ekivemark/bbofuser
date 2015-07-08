"""
developeraccount
FILE: organization
Created: 6/25/15 10:48 AM

forms related to Organization

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.shortcuts import render, get_object_or_404
from django import forms
from django.conf import settings

from accounts.models import Organization, User, USER_ROLE_CHOICES
from accounts.utils import strip_url


class Url(forms.URLField):
    def clean(self, value):
        super(Url, self).clean(value).lower()
        try:
            Organization.objects.get(site_url=value)
            primary_email = "[Add function here]"
            backup_email =  "[Add email obscuring function here]"

            validation_msg = "This organization is already registered."
            validation_msg = validation_msg + " Contact "
            validation_msg = validation_msg + primary_email + " or "
            validation_msg = validation_msg + backup_email
            validation_msg = validation_msg + " for an invitation to join the organization"

            raise forms.ValidationError(validation_msg)
        except Organization.DoesNotExist:
            return value


class OrganizationCheckForm(forms.Form):
    """
    A form for checking an Organization top level url
    """
#    site_url = forms.CharField(label="Organization URL",
#                               help_text="enter the top level organization domain. eg. domain.com")

    domain = Url(label="Organization Domain",
                   help_text="<br/>Enter the top level organization domain. <br/>eg. domain.com")
    if settings.DEBUG:
        print "in OrganizationCheckForm"

    def clean_domain(self):

        print "checking for this:" , self.cleaned_data['domain']
        check_for = strip_url(self.cleaned_data['domain'],"www")
        #check_for = check_for.replace("http://","")
        #check_for = check_for.replace("https://","")
        #check_for = check_for.replace("www.","")

        print "Check_for:", check_for

        try:
            org_compare = Organization.objects.get(domain=check_for)
        except:
            print check_for, "Domain Not Found. That is good!"
            return check_for

        print "[", org_compare, "]"
        if (org_compare.domain.lower() == check_for):

            print "matched on ", org_compare.domain

            primary_email = "[Add function here]"
            backup_email =  "[Add email obscuring function here]"

            validation_msg = "This domain is already registered."
            validation_msg = validation_msg + " Contact "
            validation_msg = validation_msg + primary_email + " or "
            validation_msg = validation_msg + backup_email
            validation_msg = validation_msg + " for an invitation to join the organization"

            raise forms.ValidationError(validation_msg)
        else:
            print "Domain does not exist"
            print "(%s)" % check_for
            return check_for

