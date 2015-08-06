"""
BBonFHIRUser
FILE: organization
Created: 7/8/15 1:20 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext

from accounts.decorators import session_master
from accounts.forms.application import Application_EditForm
from accounts.models import Application


@session_master
@login_required
def application_edit(request, pk):
    if settings.DEBUG:
        print(request.user)
        print("Entering Application Edit with:%s" % pk)

    a = Application.objects.get(pk=pk)

    if settings.DEBUG:
        print("Application:", a)

    form = Application_EditForm(data=request.POST or None, instance=a)

    if request.POST:
        form = Application_EditForm(request.POST)
        if form.is_valid():

            if settings.DEBUG:
                print("Form is valid - current record:", a)

            # Update OrgApplication here

            a.redirect_uris = form.cleaned_data['redirect_uris']
            a.client_type = form.cleaned_data['client_type']
            a.authorization_grant_type = form.cleaned_data[
                'authorization_grant_type']
            a.skip_authorization = form.cleaned_data['skip_authorization']

            # Update Fields above
            if settings.DEBUG:
                print("Updated to:", a)
            a.save()

            return HttpResponseRedirect(reverse('accounts:manage_account'),
                                        RequestContext(request))
        else:

            if settings.DEBUG:
                print("Form is invalid")

            messages.error(request, "There was an input problem.")
            return render(request, 'accounts/application_edit.html',
                          {'form': form, 'application': a.name, })

    else:
        a = Application.objects.get(pk=pk)

        if settings.DEBUG:
            print("in the get with Organization:", a.name, " ", a.name, )
        form = Application_EditForm(initial={'client_type': a.client_type,
                                             'authorization_grant_type': a.authorization_grant_type,
                                             'redirect_uris': a.redirect_uris,
                                             'skip_authorization': a.skip_authorization, })
        if settings.DEBUG:
            print("Not in the post in the get")
        return render(request, 'accounts/application_edit.html',
                      {'form': form,
                       'application': a.name})
