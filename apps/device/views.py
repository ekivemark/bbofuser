"""
bbofuser:device
FILE: views
Created: 8/3/15 6:54 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from uuid import uuid4
from django.conf import settings
from django.views.generic.edit import DeleteView
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import (render_to_response, redirect)
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext

from apps.device.models import Device
from apps.device.forms import (Device_EditForm,
                                Device_View)
from apps.device.utils import get_phrase
from datetime import datetime, timedelta


def device_index(request):
    # Show Device Home Page

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print(settings.APPLICATION_TITLE, "in apps.device.views.device_index")

    context = {}
    return render_to_response('device/index.html',
                              RequestContext(request, context, ))


@login_required()
def device_add(request):

    if settings.DEBUG:
        print("In apps.device.views.device_add")

    if request.POST:
        form = Device_EditForm(request.POST)
        if form.is_valid():
            if settings.DEBUG:
                print("Form is valid. Adding Device")

            d = Device()

            d.user = request.user
            d.password = form.cleaned_data['password']
            d.device = form.cleaned_data['device']
            d.account = form.cleaned_data['account']
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


@login_required()
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

            if settings.DEBUG:
                print("Form is valid - current record:", d)

            # Update Device here

            d.device = form.cleaned_data['device']
            d.account = form.cleaned_data['account']
            d.password = form.cleaned_data['password']
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


class Device_Delete(DeleteView):
    model = Device
    success_url = reverse_lazy('accounts:manage_account')



