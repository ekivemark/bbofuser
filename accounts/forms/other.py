"""
accounts
FILE: forms.py
Created: 6/21/15 8:31 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.shortcuts import render, get_object_or_404
from django import forms
from registration.forms import RegistrationFormUniqueEmail, RegistrationFormTermsOfService

from accounts.models import User, Agreement, Organization


class Email(forms.EmailField):
    def clean(self, value):
        super(Email, self).clean(value)
        try:
            User.objects.get(email=value)
            raise forms.ValidationError("This email is already registered. Use the 'forgot password' link on the login page")
        except User.DoesNotExist:
            return value


class UserRegistrationForm(forms.Form):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(widget=forms.PasswordInput(), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Repeat your password")
    #email will be become username
    email = Email()

    def clean_password(self):
        if self.data['password1'] != self.data['password2']:
            raise forms.ValidationError('Passwords are not the same')
        return self.data['password1']


class RegistrationFormUserTOSAndEmail(UserRegistrationForm,
                                      RegistrationFormUniqueEmail,
                                      RegistrationFormTermsOfService):
    pass


class RegistrationFormTOSAndEmail(
                                  RegistrationFormUniqueEmail,
                                  RegistrationFormTermsOfService):
    pass


def agreement_view(request, mymodel_id):
    class MyModelForm(forms.ModelForm):
        class Meta:
            model = Agreement

    model = get_object_or_404(Agreement, pk=mymodel_id)
    form = MyModelForm(instance=model)
    return render(request, 'developer/model.html', { 'form': form})


def organization_view(request, mymodel_id):
    class MyModelForm(forms.ModelForm):
        class Meta:
            model = Organization

    model = get_object_or_404(Organization, pk=mymodel_id)
    form = MyModelForm(instance=model)
    return render(request, 'developer/model.html', { 'form': form})

