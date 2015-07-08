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
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import make_aware
from django.contrib.auth import login as django_login, authenticate, logout as django_logout

from accounts.models import OrgApplication, Agreement, Organization, User, ValidSMSCode
from accounts.forms.authenticate import AuthenticationForm, SMSCodeForm, AuthenticationSMSForm

from accounts.admin import UserCreationForm
from accounts.utils import strip_url, cell_email
from django.contrib import messages


def validate_sms(username, smscode):

    if settings.DEBUG:
        print("%s, %s" % (username, smscode))

    mfa_on = False
    try:
        u = User.objects.get(email=username)
        mfa_on = u.mfa
        vc = ValidSMSCode.objects.get(user=u, sms_code=smscode)
        if settings.DEBUG:
            print("vc: %s - %s" % (vc, mfa_on))
        now = timezone.now()
        if vc.expires < now:
            vc.delete()
            return False
    except(User.DoesNotExist):
        if settings.DEBUG:
            print("User does not exist")
        return False
    except(ValidSMSCode.DoesNotExist):
        if not mfa_on:
            if settings.DEBUG:
                print("MFA disabled","")
            return True
        else:
            if settings.DEBUG:
                print("ValidSMS does not exist")
            return False
    if settings.DEBUG:
        print("Success! Deleting %s" % vc)
    vc.delete()
    return True


def sms_login(request, email="", *args, **kwargs):
    if settings.DEBUG:
        print(request.GET)
        print("SMS_LOGIN.GET:email:[%s]" % (email))
        print(request.POST)
        print(args)


    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if request.POST['login'].lower() == 'resend code':
            if settings.DEBUG:
                print("Resending Code for %s" % request.POST['email'])
            form = SMSCodeForm(request.POST)
            form.email = request.POST['email']
            args = {}
            args['form'] = form
            return render_to_response('accounts/smscode.html',
                                      RequestContext(request, args))
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
            print("in sms_login. Setting up Form")
            print("email:%s" % email)
        form = AuthenticationForm(initial={'email':email})
    return render_to_response('accounts/login.html', {'form': AuthenticationForm()},
                              RequestContext(request))

def sms_code(request, email=""):

    status = "NONE"
    if settings.DEBUG:
        print("in accounts.views.sms.sms_code")
        print("Email:", email)

    if request.method == 'POST':
        if request.POST.__contains__('email'):
            email = request.POST['email']
            print("POST email on entry:[%s]" % (email))
    if request.method == 'POST':
        if settings.DEBUG:
            print("request.POST:%s" % request.POST)
            print("POST email:%s" % request.POST['email'])

        form = SMSCodeForm(request.POST)

        if form.is_valid():
            try:
                u=User.objects.get(email=form.cleaned_data['email'])
                mfa_required = u.mfa
                email_address = u.email
                if settings.DEBUG:
                    print("Require MFA Login:%s" % mfa_required)
                if u.is_active:
                    if mfa_required:
                        ValidSMSCode.objects.create(user=u)
                        messages.success(request, "A text message was sent to your mobile phone.")
                        status = "Text Message Sent"
                    else:
                        messages.success(request, "Your account is active. Continue Login.")
                        status = "Account Active"
                else:
                    messages.error(request, "Your account is inactive.")
                    status = "Inactive Account"
                    return HttpResponseRedirect(reverse('accounts:sms_code'))
            except(User.DoesNotExist):
                messages.error(request, "You are not recognized.")
                status = "User UnRecognized"
                return HttpResponseRedirect(reverse('accounts:sms_code'))
                # except(UserProfile.DoesNotExist):
                #     messages.error(request, "You do not have a user profile.")
                #     return HttpResponseRedirect(reverse('sms_code'))
            if settings.DEBUG:
                print("dropping out of valid form")
                print("Status:", status)
                print("email Address: %s" % email_address)
            # Change the form and move to login
            form = AuthenticationForm(initial={'email':email_address})
            args = {}
            args['form'] = form
            return HttpResponseRedirect(reverse('accounts:login'),args )
        else:
            if settings.DEBUG:
                print("invalid form")
            form.email = email

            return render_to_response('accounts/login.html',
                                      RequestContext(request, {'form': form}))
    else:
        if settings.DEBUG:
            print("setting up the POST in sms_code")

    return render_to_response('accounts/smscode.html',
                              context_instance = RequestContext(request))


def login_optional_sms(request):
    """
    One screen Login with SMS
    :param request:
    :return:

    Prompt for: email, password.
    Offer "Send Pin Code" and "Login" Submit buttons

    Test email and password. Check for MFA setting.
    If MFA is enabled and Login button used with no Pin Code then fail validation
    If User and Password are correct and no MFA then allow login

    If User and Password and MFA and Pin Code then allow Login

    Else fail validation


    """

    if settings.DEBUG:
        print("in accounts.views.sms.login_optional_sms")

    if request.method == 'POST':
        # handle the form input
        if settings.DEBUG:
            print("in the POST")
        form = AuthenticationSMSForm(request.POST)

        # check for Login Method:
        # 1. = Login
        # 2. = Send Pin Code
        if request.POST['login'].lower() == 'send pin code':
            if settings.DEBUG:
                print("Sending Code to %s" % (request.POST['email']))

            try:
                u = User.objects.get(email = request.POST['email'])
            except User.DoesNotExist:
                messages.error(request, "Something went wrong.")
                form = AuthenticationSMSForm(request.POST)
                form.email = request.POST['email']
                return render_to_response('accounts/login_sms.html',
                                          {'form': form},
                                            RequestContext(request))
            mfa_required = u.mfa
            email_address = u.email

            if u.is_active:
                form = AuthenticationSMSForm()
                form.email = email_address

                if mfa_required:
                    ValidSMSCode.objects.create(user=u)
                    messages.success(request, "A text message was sent to your mobile phone.")
                else:
                    messages.success(request, "Your account is active. Continue Login.")
            return render_to_response('accounts/login_sms.html',
                                      RequestContext(request,{'form': form} ))

        elif request.POST['login'].lower() == 'login':
            if settings.DEBUG:
                print("in login step")

        if form.is_valid:
            if settings.DEBUG:
                print("Valid form received")
            # print "Authenticate"
            email = form.cleaned_data.get['email']
            password = form.cleaned_data.get['password']
            sms_code = form.cleaned_data.get['sms_code']
            if not validate_sms(username=email, smscode=sms_code):
                messages.error(request, "Invalid Access Code.")
                return render_to_response('accounts/login_sms.html',
                                          {'form': AuthenticationSMSForm()},
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
            # form is not valid
            form.email = form.cleaned_data['email']
            form.password = form.cleaned_data['password']
            render_to_response('accounts/login_sms.html',
                              context_instance = RequestContext(request, {'form':form},))
    else:
        # setup the form. We are entering with a GET to the page.
        if settings.DEBUG:
            print("setting up sms.login_optional_sms form")
        form = AuthenticationSMSForm
    return render_to_response('accounts/login_sms.html',
                              context_instance = RequestContext(request, {'form':form},))

def login_optional(request):
    """
    One screen Login with SMS
    :param request:
    :return:

    Prompt for: email, password.
    Offer "Send Pin Code" and "Login" Submit buttons

    Test email and password. Check for MFA setting.
    If MFA is enabled and Login button used with no Pin Code then fail validation
    If User and Password are correct and no MFA then allow login

    If User and Password and MFA and Pin Code then allow Login

    Else fail validation


    """
    args = {}
    if settings.DEBUG:
        print("in accounts.views.sms.login_optional")

    if request.POST:
        form = AuthenticationSMSForm(request.POST)
        if settings.DEBUG:
            print("test login before is_valid()")
            print(request.POST['login'])

            print("pin needed? [%s]" % request.POST['send_pin'])
        if form.is_valid():
            if settings.DEBUG:
                print("in the post section with form instance")
                print(form)
                print("Email:", form.cleaned_data['email'])
            # Do the evaluation logic here
            if request.POST['login'].lower() == 'send pin code':
                if settings.DEBUG:
                    print("Sending PIN")
                try:
                    u = User.objects.get(email = request.POST['email'])
                except User.DoesNotExist:
                    messages.error(request, "Something went wrong.")
                    form = AuthenticationSMSForm(request.POST)
                    form.email = request.POST['email']
                    return render_to_response('accounts/login_sms.html',
                                            RequestContext(request,{'form': form},))
            else:
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                sms_code = form.cleaned_data['sms_code']
                if not validate_sms(username=email, smscode=sms_code):
                    messages.error(request, "Invalid Access Code.")
                    return render_to_response('accounts/login_sms.html',
                                              {'form': AuthenticationForm()},
                                              RequestContext(request))

                user=authenticate(username=email, password=password)

                if user is not None:

                    if user.is_active:
                        django_login(request, user)
                        return HttpResponseRedirect(reverse('home'))
                    else:

                        messages.error(request, "Your account is not active.")
                        return HttpResponseRedirect(reverse('login_sms'))
                else:
                    messages.error(request, "Invalid username or password.")
                    return render_to_response('accounts/login_sms.html',
                                          {'form': AuthenticationForm()},
                                          RequestContext(request))
        else:            # FORM IS NOT VALID
            if settings.DEBUG:
                print("Form is invalid")
            args['form'] = form
            return render(request, 'accounts/login_sms.html', args )

    else: # Not a POST
        form = AuthenticationSMSForm()
        return render_to_response('accounts/login_sms.html',
                                  context_instance=RequestContext(request,
                                                                  {'form': form}))
