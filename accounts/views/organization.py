"""
devaccount3
FILE: organization
Created: 7/8/15 1:20 PM


"""
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.db.models import Q
from accounts.models import User, Organization, OrgApplication
from accounts.forms.organization import Organization_EditForm
from accounts.forms.application import OrgApplication_EditForm


__author__ = 'Mark Scrimshire:@ekivemark'


@login_required()
def organization_edit(request):

    if settings.DEBUG:
        print(request.user)
        print("Entering Organization Edit with:%s" % request.user.email)

    u = User.objects.get(email=request.user.email)
    org_list = Organization.objects.filter(Q(owner=u) | Q(alternate_owner=u))
    o = org_list[:1].get()
    if settings.DEBUG:
        print("User Affiliation:", u.affiliated_to)
        print("Organizations:", org_list)

    if settings.DEBUG:
        print("User returned:", u, "[", u.affiliated_to.id, "]")
        print("Organization:", o, " key:", o.pk)

    form = Organization_EditForm(data = request.POST or None, instance=o)

    if request.POST:
        form = Organization_EditForm(request.POST)
        if form.is_valid():

            if settings.DEBUG:
                print("Form is valid - current record:", u)

            # Update Organization here

            o.name = form.cleaned_data['name']
            o.privacy_url = form.cleaned_data['privacy_url']



            # Update Fields above
            if settings.DEBUG:
                print("Updated to:", u)
            o.save()

            return HttpResponseRedirect(reverse('accounts:manage_account'),
                                        RequestContext(request))
        else:

            if settings.DEBUG:
                print("Form is invalid")

            messages.error(request, "There was an input problem.")
            return render(request, 'accounts/organization_edit.html',
                          {'form':form,'organization': o.domain,})

    else:
        u = User.objects.get(email=request.user.email)
        org_list = Organization.objects.filter(Q(owner=u) | Q(alternate_owner=u))
        o = org_list[:1].get()

        if settings.DEBUG:
            print("in the get with Organization:",o.name," ", o.domain,)
        form = Organization_EditForm(initial={'name':o.name, 'domain':o.domain,
                                              'site_url': o.site_url,
                                              'privacy_url': o.privacy_url})
        if settings.DEBUG:
            print("Not in the post in the get")
        return render(request, 'accounts/organization_edit.html',
                                                 {'form': form,
                                                  'organization': o.domain})


@login_required()
def orgapplication_edit(request, pk):

    if settings.DEBUG:
        print(request.user)
        print("Entering Application Edit with:%s" % pk)


    a = OrgApplication.objects.get(pk=pk)

    if settings.DEBUG:
        print("Application:",a)

    form = OrgApplication_EditForm(data = request.POST or None, instance=a)

    if request.POST:
        form = OrgApplication_EditForm(request.POST)
        if form.is_valid():

            if settings.DEBUG:
                print("Form is valid - current record:", a)

            # Update OrgApplication here

            a.redirect_uris = form.cleaned_data['redirect_uris']
            a.icon_link = form.cleaned_data['icon_link']
            a.client_type = form.cleaned_data['client_type']
            a.authorization_grant_type = form.cleaned_data['authorization_grant_type']
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
            return render(request, 'accounts/orgapplication_edit.html',
                          {'form':form,'application': a.name,})

    else:
        a = OrgApplication.objects.get(pk=pk)

        if settings.DEBUG:
            print("in the get with Organization:",a.name," ", a.name,)
        form = OrgApplication_EditForm(initial={'icon_link': a.icon_link,
                                                'client_type': a.client_type,
                                                'authorization_grant_type': a.authorization_grant_type,
                                                'redirect_uris':a.redirect_uris,
                                                'skip_authorization': a.skip_authorization,})
        if settings.DEBUG:
            print("Not in the post in the get")
        return render(request, 'accounts/orgapplication_edit.html',
                                                 {'form': form,
                                                  'application': a.name})


