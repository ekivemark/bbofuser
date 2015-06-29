"""
 Developer views
 (c) 2015 - Mark Scrimshire - @ekivemark
"""

# DONE Activate Account
# TODO: Manage Account
# TODO: Delete Account
# TODO: Manage Organization
# TODO: Request Application Credentials
# TODO: Manage Application Credentials
# TODO: Delete Application Credentials
# DONE: accounts/profile Landing Page.

# Work flow will use django-registration to enable Account sign up
# After Activation
from datetime import datetime
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import make_aware
from django.contrib.auth import login as django_login, authenticate, \
    logout as django_logout
from django.views.generic.detail import DetailView

from models import Application, Agreement, Organization, User, ValidSMSCode
from accounts.forms.authenticate import AuthenticationForm, SMSCodeForm
from accounts.forms.register import RegistrationForm
from accounts.forms.organization import OrganizationCheckForm
from accounts.forms.application import ApplicationCheckForm, application_view
from accounts.admin import UserCreationForm
from utils import strip_url, cell_email
from django.contrib import messages

def login(request):
    """
    Login view

    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    django_login(request, user)
                    return redirect('/')
    else:
        form = AuthenticationForm()
    return render_to_response('registration/login.html', {
        'form': form,
    }, context_instance=RequestContext(request))


def register(request):
    """
    User registration view.
    """
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse_lazy('home'))
    else:
        form = RegistrationForm()
    return render_to_response(reverse_lazy('accounts:register'), {
        'form': form,
    }, context_instance=RequestContext(request))


def logout(request):
    """
    Log out view
    """
    django_logout(request)
    return redirect(reverse_lazy('home'))


# class AccountDetailView(DetailView):
#     model = Account
#     slug_field = "id"
#
#     def get_context_data(self, **kwargs):
#         fields = [(f.verbose_name, f.name, f.value) for f in
#                   Account._meta.get_fields()]
#
#         context = super(AccountDetailView,
#                         self).get_context_data(**kwargs)
#
#         context['now'] = timezone.now()
#         context['fields'] = fields
#
#         return context


class AgreementDetailView(DetailView):
    model = Agreement
    slug_field = "id"

    def get_context_data(self, **kwargs):
        context = super(AgreementDetailView, self).\
            get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class OrganizationDetailView(DetailView):
    model = Organization
    slug_field = "id"

    def get_context_data(self, **kwargs):
        context = super(OrganizationDetailView, self).\
            get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def home_index(request):

    # Show Home Page
    application_title = settings.APPLICATION_TITLE
    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print application_title, "in accounts.views.home_index"

    context = {"APPLICATION_TITLE": application_title}
    return render_to_response('index.html', RequestContext(request, context,))


def agree_to_terms(request):

    # Agree to Terms
    # Register for account

    application_title = settings.APPLICATION_TITLE
    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print application_title, "in accounts.views.agree_to_terms"

    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse_lazy('home'))
    else:
        form = UserCreationForm()


    context = {"APPLICATION_TITLE": application_title,
               'form': form,}
    #   return render_to_response('developer/agree_to_terms.html', RequestContext(request, context,))
    return render_to_response(reverse_lazy('accounts:register'), RequestContext(request, context,))


@login_required
def manage_account(request):

    # Manage Accounts entry page

    # DONE: Remove api.data.gov signup widget in manage_account.html

    application_title = settings.APPLICATION_TITLE
    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print application_title, "in accounts.views.manage_account"
    user = request.user
    mfa_address = cell_email(user.mobile, user.carrier)

    # Get a list of organizations for this user
    # org_list = list(Organization.objects.all())
    org_list = list(Organization.objects.filter(owner=user))
    app_list = list(Application.objects.filter(owner=user))
    context = {"APPLICATION_TITLE": application_title,
               "user": user,
               "mfa_address": mfa_address,
               "organizations": org_list,
               "applications": app_list}

    return render_to_response('developer/manage_account.html',
                              RequestContext(request, context,))


# DONE: Add Connect_Organization View
# DONE: prompt for Organization top level url
# DONE: Convert url to lowercase
# DONE: Check if top level url exists in organization.site_url
# DONE: If Organization is not found open form for data input
# DONE: Update User.affiliated_to and User.organization_role
# DONE: Save Organization with link to User
# DONE: Create developer/connect_organization.html
# DONE: Add view to accounts/urls.py

@login_required()
def connect_organization(request):
    """
    Connect organization and user
    :param request:
    :return:
    """

    user = request.user
    application_title = settings.APPLICATION_TITLE

    context = {"APPLICATION_TITLE": application_title,
               "user": user}

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print application_title, "in accounts.views.connect_organization"
        print "request.method:"
        print request.method
        print request.POST

    if request.method == 'POST':
        form = OrganizationCheckForm(data=request.POST)

        if form.is_valid():
            if DEBUG:
                print "form is valid"
                print "form", form.cleaned_data['domain']
            org = Organization()
            org.domain = form.cleaned_data['domain']
            org.site_url = "http://"+form.cleaned_data['domain']
            org.owner = user
            org.name = org.domain
            org.save()

            u = request.user
            if DEBUG:
                print "user", u
            u.affiliated_to = org
            u.organization_role = "primary"

            return redirect(reverse_lazy('accounts:manage_account'))
        else:
            print "OrganizationCheckForm", request.POST, " NOT Valid"
    else:
        form = OrganizationCheckForm()

    context['form'] = form

    if DEBUG:
        print context

    return render_to_response('developer/connect_organization.html',
                             context,
                              context_instance=RequestContext(request))


@login_required()
def connect_application(request):
    """
    Connect application ot Organization and User
    :param request:
    :return:
    """

    user = request.user
    application_title = settings.APPLICATION_TITLE

    context = {"APPLICATION_TITLE": application_title,
               "user": user}

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print application_title, "in accounts.views.connect_application"
        print "request.method:"
        print request.method
        print request.POST

    if request.method == 'POST':
        form = ApplicationCheckForm(data=request.POST)

        if form.is_valid():
            if DEBUG:
                print "form is valid"
                print "form", form.cleaned_data
            app = Application()
            app.name = form.cleaned_data['name']
            app.callback = form.cleaned_data['callback'].lower()
            app.icon_link = form.cleaned_data['icon_link'].lower()

            app.owner = request.user
            app.organization = user.affiliated_to
            app.save()


            if DEBUG:
                print "user", user

            return redirect(reverse_lazy('accounts:manage_account'))
        else:
            print "ApplicationCheckForm", request.POST, " NOT Valid"
    else:
        form = ApplicationCheckForm()

    context['form'] = form

    if DEBUG:
        print context

    return render_to_response('developer/connect_application.html',
                             context,
                              context_instance=RequestContext(request))


def validate_sms(username, smscode):

    if settings.DEBUG:
        print "%s, %s" % (username, smscode)

    try:
        u = User.objects.get(email=username)
        vc = ValidSMSCode.objects.get(user=u, sms_code=smscode)
        if settings.DEBUG:
            print "vc: %s" % vc
        now = timezone.now()
        if vc.expires < now:
            vc.delete()
            return False
    except(User.DoesNotExist):
        if settings.DEBUG:
            print "User does not exist"
        return False
    except(ValidSMSCode.DoesNotExist):
        if settings.DEBUG:
            print "ValidSMS does not exist"
        return False
    if settings.DEBUG:
        print "Success! Deleting %s" % vc
    vc.delete()
    return True


def sms_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
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
    return render_to_response('accounts/login.html', {'form': AuthenticationForm()},
                              RequestContext(request))

def sms_code(request):

    if settings.DEBUG:
        print "in accounts.views.sms_code"
    if request.method == 'POST':
        if settings.DEBUG:
            print "request.POST:%s" % request.POST
        form = SMSCodeForm(request.POST)
        if form.is_valid():
            try:
                u=User.objects.get(email=form.cleaned_data['email'])
                mfa_required = u.mfa
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
                return HttpResponseRedirect(reverse('sms_code'))
                # except(UserProfile.DoesNotExist):
                #     messages.error(request, "You do not have a user profile.")
                #     return HttpResponseRedirect(reverse('sms_code'))
            return HttpResponseRedirect(reverse('accounts:login'))

        else:
            return render_to_response('accounts/smscode.html',
                                      RequestContext(request, {'form': form}))

    return render_to_response('accounts/smscode.html',
                              context_instance = RequestContext(request))