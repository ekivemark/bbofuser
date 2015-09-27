"""
 Developer views
 (c) 2015 - Mark Scrimshire - @ekivemark
"""
__author__ = 'Mark Scrimshire:@ekivemark'

# DONE Activate Account
# DONE: accounts/profile Landing Page.
import ast
import json

from collections import OrderedDict
from django.core import serializers
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth import (login as django_login,
                                 authenticate,
                                 logout as django_logout)
from django.views.generic.detail import DetailView

from accounts.admin import UserCreationForm
from accounts.decorators import (session_master,
                                 session_master_required)
from accounts.forms.application import (ApplicationCheckForm)
from accounts.forms.authenticate import AuthenticationForm
from accounts.forms.register import RegistrationForm
from accounts.models import (Application,
                             Crosswalk)
from accounts.utils import (cell_email,
                            send_activity_message)

from apps.bluebutton.cms_parser_utilities import string_to_ordereddict

from apps.subacc.models import Device
from apps.subacc.utils import Master_Account

from apps.secretqa.models import QA


def login(request):
    """
    Login view

    """
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(email=request.POST['email'],
                                password=request.POST['password'])
            if user is not None:
                if settings.DEBUG:
                    print("User is not Empty!")
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
    context = {'form': form}

    return render_to_response('register.html',
                              context_instance=RequestContext(request,
                                                              context,))


def logout(request):
    """
    Log out view
    """
    # DONE: Change redirection based on whether subacc or user
    if 'auth_device' in request.session:
        mode = "subacc"
    else:
        mode = "user"

    django_logout(request)
    if mode == "subacc":
        return redirect(reverse_lazy('api:home'))
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


def home_index(request):
    # Show Home Page

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print(settings.APPLICATION_TITLE, "in accounts.views.other.home_index")

    context = {}
    return render_to_response('index.html',
                              RequestContext(request, context, ))


def about(request):
    # Show About Page

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print(settings.APPLICATION_TITLE, "in accounts.views.other.about")

    context = {}
    return render_to_response('about.html',
                              RequestContext(request, context, ))


def agree_to_terms(request):
    # Agree to Terms
    # Register for account

    if settings.DEBUG:
        print(settings.APPLICATION_TITLE,
              "in accounts.views.agree_to_terms")

    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(reverse_lazy('home'))
    else:
        form = UserCreationForm()

    context = {'form': form, }
    #   return render_to_response('developer/agree_to_terms.html', RequestContext(request, context,))
    return render_to_response(reverse_lazy('accounts:register'),
                              RequestContext(request, context, ))

@session_master
@login_required
def manage_account(request):
    # Manage Accounts entry page

    # DONE: Remove api.data.gov signup widget in manage_account.html

    if settings.DEBUG:
        print(settings.APPLICATION_TITLE,
              "in accounts.views.manage_account")
    user = request.user
    mfa_address = cell_email(user.mobile, user.carrier)

    dev_list = list(Device.objects.filter(user_id=request.user,
                                          deleted=False))
    # DONE: Get Device Used indicator
    # Used Field is included in Device. It is set during login
    try:
        xwalk = Crosswalk.objects.get(user=request.user)
        mmg_xwalk = {}
        mmg_xwalk['mmg_user'] = xwalk.mmg_user
        mmg_xwalk['mmg_name'] = xwalk.mmg_name
        mmg_xwalk['mmg_email'] = xwalk.mmg_email
        mmg_xwalk['mmg_account'] = xwalk.mmg_account
        mmg_xwalk['mmg_bbdata'] = xwalk.mmg_bbdata
        mmg_xwalk['mmg_bbfhir'] = xwalk.mmg_bbfhir

        temp = xwalk.mmg_bbjson
        # if settings.DEBUG:
            # print("Temp:", temp)
        #temp2 = json.loads(eval(temp))
        #temp = json.loads(json.dumps(xwalk.mmg_bbjson),object_pairs_hook=OrderedDict)
        #temp = json.dumps(serializers.serialize(xwalk.mmg_bbjson))

        #print("Temp2:", temp2)
        #print("========")
        #for key, value in temp2.items():
        #    print("Key:", key, ":", temp[key])

        mmg_xwalk['mmg_bbjson'] = temp
        # print("patient:", temp['patient'])
    except Crosswalk.DoesNotExist:
        mmg_xwalk = {}

    try:
        secretqa = QA.objects.get(user=request.user)
    except QA.DoesNotExist:
        secretqa = None
    if settings.DEBUG:
        print("secretqa-QA",secretqa)

    if secretqa == None:
        security_mode = "add"
    else:
        security_mode = "edit"

    security_list = secretqa
    context = {"user": user,
               "mfa_address": mfa_address,
               "mmg_xwalk": mmg_xwalk,
               "devices": dev_list,
               'security_mode': security_mode,
               "security": security_list}

    return render_to_response('accounts/manage_account.html',
                              RequestContext(request, context, ))


# DONE: Add Connect_Organization View
# DONE: prompt for Organization top level url
# DONE: Convert url to lowercase
# DONE: Check if top level url exists in organization.site_url
# DONE: If Organization is not found open form for data input
# DONE: Update User.affiliated_to and User.organization_role
# DONE: Save Organization with link to User
# DONE: Create developer/connect_organization.html
# DONE: Add view to accounts/urls.py.py


@session_master
@login_required
def connect_application(request):
    """
    Connect application to Organization and User
    :param request:
    :return:
    """

    user = request.user
    application_title = settings.APPLICATION_TITLE

    context = {"user": user}

    if settings.DEBUG:
        print(application_title, "in accounts.views.connect_application")
        print("request.method:")
        print(request.method)
        print(request.POST)

    if request.method == 'POST':
        form = ApplicationCheckForm(data=request.POST)

        if form.is_valid():
            if settings.DEBUG:
                print("form is valid")
                print("form", form.cleaned_data)

            app = Application()
            app.name = form.cleaned_data['name']
            app.callback = form.cleaned_data['callback'].lower()
            app.owner = request.user
            app.user_id = request.user.id

            if settings.DEBUG:
                print("OrgApp:", app, app.owner, user)

            app.save()

            if settings.DEBUG:
                print("user", user)

            return redirect(reverse_lazy('accounts:manage_account'))
        else:
            print("ApplicationCheckForm", request.POST, " NOT Valid")
    else:
        form = ApplicationCheckForm()

    context['form'] = form

    if settings.DEBUG:
        print("Loading Render toResponse in accounts.views.other.connect_application")

    return render_to_response('accounts/connect_application.html',
                              context,
                              context_instance=RequestContext(request))

@session_master
@login_required
class Application_Detail(DetailView):
    model = Application


