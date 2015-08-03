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
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.conf import settings
from django.contrib.auth import (login as django_login,
                                 authenticate,
                                 logout as django_logout)
from django.views.generic.detail import DetailView

from accounts.models import Application
from accounts.forms.authenticate import AuthenticationForm
from accounts.forms.register import RegistrationForm
from accounts.forms.application import (ApplicationCheckForm)
from accounts.admin import UserCreationForm
from accounts.utils import cell_email


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

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
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


@login_required
def manage_account(request):
    # Manage Accounts entry page

    # DONE: Remove api.data.gov signup widget in manage_account.html

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print(settings.APPLICATION_TITLE,
              "in accounts.views.manage_account")
    user = request.user
    mfa_address = cell_email(user.mobile, user.carrier)

    app_list = list(Application.objects.filter(user=user))
    context = {"user": user,
               "mfa_address": mfa_address,
               "applications": app_list}

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
# DONE: Add view to accounts/urls.py


@login_required()
def connect_application(request):
    """
    Connect application to Organization and User
    :param request:
    :return:
    """

    user = request.user
    application_title = settings.APPLICATION_TITLE

    context = {"user": user}

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print(application_title, "in accounts.views.connect_application")
        print("request.method:")
        print(request.method)
        print(request.POST)

    if request.method == 'POST':
        form = ApplicationCheckForm(data=request.POST)

        if form.is_valid():
            if DEBUG:
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

            if DEBUG:
                print("user", user)

            return redirect(reverse_lazy('accounts:manage_account'))
        else:
            print("ApplicationCheckForm", request.POST, " NOT Valid")
    else:
        form = ApplicationCheckForm()

    context['form'] = form

    if DEBUG:
        print(context)

    return render_to_response('accounts/connect_application.html',
                              context,
                              context_instance=RequestContext(request))


class Application_Detail(DetailView):
    model = Application
