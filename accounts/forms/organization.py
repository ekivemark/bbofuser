"""
developeraccount
FILE: organization
Created: 6/25/15 10:48 AM

forms related to Organization

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.shortcuts import render, get_object_or_404
from django import forms

from accounts.models import Organization, User, USER_ROLE_CHOICES


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

    site_url = Url(label="Organization URL",
                   help_text="<br/>Enter the top level organization domain. <br/>eg. domain.com")
    print "in OrganizationCheckForm"

    def clean_site_url(self):

        check_for = self.cleaned_data['site_url'].lower()
        check_for = check_for.replace("http://","")
        check_for = check_for.replace("https://","")
        check_for = check_for.replace("www.","")

        print "Check_for:", check_for

        org_compare = Organization(site_url=check_for)
        print "[", org_compare, "]"
        if (org_compare.site_url.lower() == check_for):

            print "matched on ", org_compare.site_url

            primary_email = "[Add function here]"
            backup_email =  "[Add email obscuring function here]"

            validation_msg = "This organization is already registered."
            validation_msg = validation_msg + " Contact "
            validation_msg = validation_msg + primary_email + " or "
            validation_msg = validation_msg + backup_email
            validation_msg = validation_msg + " for an invitation to join the organization"

            raise forms.ValidationError(validation_msg)
        else:
            print "Organization does not exist"
            print "(%s)" % check_for

            return check_for

