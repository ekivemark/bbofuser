"""
bbofuser:device
FILE: views
Created: 8/3/15 6:54 PM

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from datetime import datetime, timedelta
from uuid import uuid4

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (get_user_model,
                                 login as django_login,
                                 authenticate as django_authenticate,
                                 logout as django_logout)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import (reverse,
                                      reverse_lazy)
from django.http import HttpResponseRedirect
from django.shortcuts import (render,
                              render_to_response,
                              redirect)
from django.template import RequestContext

from accounts.models import User
from accounts.decorators import session_master

from apps.device.models import (Device,
                                DeviceAccessLog)
from apps.device.forms import (Device_AuthenticationForm,
                               Device_EditForm,
                               Device_AddForm,
                               Device_View,
                               unique_account)
from apps.device.utils import (get_phrase,
                               session_device,
                               via_device,
                               Master_Account)


@session_master
@login_required
def device_index(request):
    # Show Device Home Page

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print(settings.APPLICATION_TITLE, "in apps.device.views.device_index")

    context = {}
    return render_to_response('device/index.html',
                              RequestContext(request, context, ))


@session_master
@login_required
def device_add(request):

    if settings.DEBUG:
        print("In apps.device.views.device_add")

    if request.POST:
        form = Device_AddForm(request.POST)
        if form.is_valid():
            if settings.DEBUG:
                print("Form is valid. Adding Device")

            d = Device()

            # DONE: Force Account and password to Lower Case
            d.user = request.user
            d.password = form.cleaned_data['password'].strip().lower()
            d.device = form.cleaned_data['device']
            # account needs to be unique
            d.account = form.cleaned_data['account'].strip().lower()
            d.valid_until = form.cleaned_data['valid_until']

            d.save()

            return HttpResponseRedirect(reverse('accounts:manage_account'),
                                        RequestContext(request))
        else:
            messages.error(request,"Did you use a device name?")
            return render(request, 'device/device_add.html',
                          {'form': form,
                           })
    else:
        acc = get_phrase(count=2)
        pwd = str(uuid4().urn)[9:]
        until_date = datetime.now()+timedelta(days=settings.DEFAULT_VALID_UNTIL)
        if settings.DEBUG:
            print("Account:",acc)
            print("Password:", pwd)

        form = Device_EditForm(initial={'account':acc,
                                        'password':pwd,
                                        'valid_until': until_date})



    return render(request,
                  'device/device_add.html',
                  {'form': form,
                   'password': pwd, }
                  )


@session_master
@login_required
def device_edit(request, pk):
    if settings.DEBUG:
        print(request.user)
        print("Entering Device Edit with:%s" % pk)

    d = Device.objects.get(pk=pk)

    if settings.DEBUG:
        print("Device", d)

    form = Device_EditForm(data=request.POST or None, instance=d)

    if request.POST:
        form = Device_EditForm(request.POST)
        if form.is_valid():
            if d.account != form.cleaned_data['account']:
                if not unique_account(form.cleaned_data['account']):

                    messages.error(request,"Account Name changed and is NOT Unique")
                    return render(request, 'device/device_edit.html',
                          {'form': form, 'device': d.device, })

            if settings.DEBUG:
                print("Form is valid - current record:", d)

            # Update Device here

            # DONE: Force Account and password to Lower Case
            d.device = form.cleaned_data['device']
            d.account = form.cleaned_data['account'].strip().lower()
            d.password = form.cleaned_data['password'].strip().lower()
            d.valid_until = form.cleaned_data['valid_until']

            # Update Fields above
            if settings.DEBUG:
                print("Updated to:", d)
            d.save()

            return HttpResponseRedirect(reverse('accounts:manage_account'),
                                        RequestContext(request))
        else:

            if settings.DEBUG:
                print("Form is invalid")

            messages.error(request, "There was an input problem.")
            return render(request, 'device/device_edit.html',
                          {'form': form, 'device': d.device, })

    else:
        d = Device.objects.get(pk=pk)

        if settings.DEBUG:
            print("in the get with Device:", d.device, )
        form = Device_EditForm(initial={'device': d.device,
                                        'account': d.account,
                                        'password': d.password,
                                        'valid_until': d.valid_until,
                                             })
        if settings.DEBUG:
            print("Not in the post in the get")
        return render(request, 'device/device_edit.html',
                      {'form': form,
                       'device': d})

@session_master
@login_required
def Device_Delete(request, pk):
    """
    We will not delete. Instead we will flag as deleted.
    This will avoid user accounts being reused
    """
    if settings.DEBUG:
        print("in apps.device.views.Device_Delete")
        print("Device:", pk,)

    d = Device.objects.get(pk=pk)

    if request.POST:
        form = Device_EditForm()
        if form.is_valid:
            if settings.DEBUG:
                print("in the POST")
            d.deleted = True
            d.save()
            return HttpResponseRedirect(reverse('accounts:manage_account'),
                                        RequestContext(request))

        else:
            if settings.DEBUG:
                print("Form is invalid")

            messages.error(request, "There was an input problem.")
            return render(request, 'device/device_confirm_delete.html',
                          {'form': form, 'device': d.device, })
    else:
        d = Device.objects.get(pk=pk)
        if settings.DEBUG:
            print("in the get with Device Deletion:", pk)
        form =Device_EditForm()

    return render(request, 'device/device_confirm_delete.html',
                    {'form': form,
                     'device': d})


def device_authenticate(account, password):
    """
    Check for Device Login
    """
    result = None

    try:
        D = Device.objects.get(account=account,
                           password=password,
            # DONE: Ignore Deleted Devices
            # DONE: We check for an active device later
                           active=True,
                           deleted=False)
        if settings.DEBUG:
            print("Matched:", account,"=", D.account)
            print("Pwd Match:", password, "=", D.password)
            print("Active:", D.is_active(), " Deleted:", D.is_deleted())
        result = D
    except Device.DoesNotExist:
        if settings.DEBUG:
            print("device_authenticate: Device.DoesNotExist")
        result = None

    if settings.DEBUG:
        print("Result:", result)
    return result


# DONE: Post Device Access Record
def Post_Device_Access(request, device):
    """

    Add the record of a device access to the DeviceAccessLog

    :param device:
    :return:
    """

    # TODO: Query DAL for Device entries older than settings.DEVICE_ACCESS_LOG_DAYS
    if not settings.DEVICE_ACCESS_LOG_DAYS:
        oldest_days = 365
    else:
        oldest_days = settings.DEVICE_ACCESS_LOG_DAYS

    if settings.DEBUG:
        print("Device:", device)

    DAL = DeviceAccessLog()

    DAL.device  = device
    DAL.account = device.account

    if settings.DEBUG:
        print(request.META.get('HTTP_USER_AGENT', ''))
        print(len(request.META.get('HTTP_USER_AGENT', '')))

    DAL.info    = request.META.get('HTTP_USER_AGENT', '')
    DAL.source  = request.META.get('HTTP_X_FORWARDED_FOR’,''') or request.META.get('REMOTE_ADDR')

    result = DAL.save()

    # DONE: Update Device used field.
    device.used = True
    device.save()

    return result


def Device_Login(request, *args, **kwargs):
    """
    Device Login
    :param request:
    :param args:
    :param kwargs:
    :return:
    """

    if request.method == 'POST':
        form = Device_AuthenticationForm(request.POST)
        if settings.DEBUG:
            print("in apps.device.views.Device_Login POST")
        if form.is_valid():
            print("Form is Valid: Authenticating Device")
            # DONE: Remove trailing spaces
            account = form.cleaned_data['account'].strip()
            Dpassword = form.cleaned_data['password'].strip()

            device = device_authenticate(account=account,
                                         password=Dpassword,)
            if settings.DEBUG:
                print("device:", device, "\nAccount:", device.account )
                print("password:", device.password)

            if device is not None:

                if device.is_active:
                    if settings.DEBUG:
                        print("Active Device:", device.is_active())
                        print("Request.user:", request.user)
                        print("Device.user:", device.user)
                    # Now get the User Account
                    User_Model = get_user_model()
                    user = User_Model.objects.get(email=device.user)
                    # fix for user.backend attribute
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth_rslt = django_authenticate(username=user.email,
                                                    password=user.password)
                    django_login(request, user)

                    session_device(request, device.device)
                    #DONE: Record Access in DeviceAccessLog

                    dal_result = Post_Device_Access(request, device)
                    if settings.DEBUG:
                        print("Post to Device Access Log:", dal_result)

                    #DONE: Update Used Field in Device
                    device.used = True
                    device.save()

                    if settings.DEBUG:
                        print("User:", user)
                        print("Django_auth result:", auth_rslt)
                        print("Sessions:", request.session )

                    return HttpResponseRedirect(reverse('api:home'))
                else: # device.active = False
                    messages.error(request, "This is an inactive device account.")
                    return HttpResponseRedirect(reverse('api:home'))
            else: # Problem with account or password match
                messages.error(request, "Invalid device account or password.")
                return render_to_response('device/device_login.html',
                                          {'form': Device_AuthenticationForm()},
                                          RequestContext(request))
        else: # Problem with the form
            return render_to_response('device/device_login.html',
                                      {'form': form},
                                      RequestContext(request))
    else: # GET and not a POST - so setup form
        if settings.DEBUG:
            print("in Device_Login. Setting up Form")
        form = Device_AuthenticationForm()

    return render_to_response('device/device_login.html', {'form': form},
                              RequestContext(request))
