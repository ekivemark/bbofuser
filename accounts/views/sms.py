"""
developeraccount
FILE: sms
Created: 7/5/15 12:45 PM

All SMS Related views

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from datetime import datetime
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import make_aware
from django.contrib.auth import login as django_login, authenticate, \
    logout as django_logout

from accounts.models import OrgApplication, Agreement, Organization, \
    User, ValidSMSCode
from accounts.forms.authenticate import AuthenticationForm, SMSCodeForm
from accounts.admin import UserCreationForm
from accounts.utils import strip_url, cell_email
from django.contrib import messages


def validate_sms(username, smscode):

    if settings.DEBUG:
        print "%s, %s" % (username, smscode)

    try:
        u = User.objects.get(email=username)
        mfa_on = u.mfa
        vc = ValidSMSCode.objects.get(user=u, sms_code=smscode)
        if settings.DEBUG:
            print "vc: %s - %s" % (vc, mfa_on)
        now = timezone.now()
        if vc.expires < now:
            vc.delete()
            return False
    except(User.DoesNotExist):
        if settings.DEBUG:
            print "User does not exist"
        return False
    except(ValidSMSCode.DoesNotExist):
        if not mfa_on:
            if settings.DEBUG:
                print "MFA disabled" \
                      ""
            return True
        else:
            if settings.DEBUG:
                print "ValidSMS does not exist"
            return False
    if settings.DEBUG:
        print "Success! Deleting %s" % vc
    vc.delete()
    return True


def sms_login(request, email=""):
    if settings.DEBUG:
        print request.GET
        print "SMS_LOGIN.GET:email:[%s]" % (email)
        print request.POST


    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if request.POST['login'].lower() == 'resend code':
            if settings.DEBUG:
                print "Resending Code for %s" % request.POST['email']
            form = SMSCodeForm(request.POST)
            form.email = request.POST['email']
            return render_to_response('accounts/smscode.html',
                                      RequestContext(request, {'form': form}))
        if form.is_valid():
            #print "Authenticate"
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            sms_code = form.cleaned_data['sms_code']
            if not validate_sms(username=email, smscode=sms_code):
                messages.error(request, "Invalid Access Code.")
                return render_to_response('accounts/login.html',
                                          {'form': AuthenticationForm()},
                              RequestContext(request))

            user=authenticate(username=email, password=password)

            if user is not None:

                if user.is_active:
                    django_login(request, user)
                    return HttpResponseRedirect(reverse('home'))
                else:

                    messages.error(request, "Your account is not active.")
                    return HttpResponseRedirect(reverse('sms_code'))
            else:
                messages.error(request, "Invalid username or password.")
                return render_to_response('accounts/login.html',
                                          {'form': AuthenticationForm()},
                              RequestContext(request))
        else:
            return render_to_response('accounts/login.html', {'form': form},
                              RequestContext(request))
    else:
        if settings.DEBUG:
            print "in sms_login. Setting up Form"
            print "email:%s" % email
        form = AuthenticationForm(initial={'email':email})
    return render_to_response('accounts/login.html', {'form': AuthenticationForm()},
                              RequestContext(request))

def sms_code(request, email=""):

    if settings.DEBUG:
        print "in accounts.views.sms_code"
    if request.method == 'POST':
        if request.POST.__contains__('email'):
            email = request.POST['email']
            print "POST email on entry:[%s]" % (email)
    if request.method == 'POST':
        if settings.DEBUG:
            print "request.POST:%s" % request.POST
            print "POST email:%s" % request.POST['email']

        form = SMSCodeForm(request.POST)

        if form.is_valid():
            try:
                u=User.objects.get(email=form.cleaned_data['email'])
                mfa_required = u.mfa
                email_address = u.email
                if settings.DEBUG:
                    print "Require MFA Login:%s" % mfa_required
                if u.is_active:
                    if mfa_required:
                        ValidSMSCode.objects.create(user=u)
                        messages.success(request, "A text message was sent to your mobile phone.")
                    else:
                        messages.success(request, "Your account is active. Continue Login.")
                else:
                    messages.error(request, "Your account is inactive.")
                    return HttpResponseRedirect(reverse('sms_code'))
            except(User.DoesNotExist):
                messages.error(request, "You are not recognized.")
                return HttpResponseRedirect(reverse('accounts:sms_code'))
                # except(UserProfile.DoesNotExist):
                #     messages.error(request, "You do not have a user profile.")
                #     return HttpResponseRedirect(reverse('sms_code'))
            if settings.DEBUG:
                print "email Address: %s" % email_address
            return HttpResponseRedirect(reverse('accounts:login'),RequestContext(request,{'email':email_address}))

        else:
            form.email = email
            return render_to_response('accounts/smscode.html',
                                      RequestContext(request, {'form': form}))
    else:
        if settings.DEBUG:
            print "setting up the POST in sms_code"

    return render_to_response('accounts/smscode.html',
                              context_instance = RequestContext(request))