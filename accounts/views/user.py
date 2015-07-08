"""
developeraccount
FILE: user
Created: 7/6/15 9:39 PM


"""
from django.contrib.auth.decorators import login_required

__author__ = 'Mark Scrimshire:@ekivemark'

from django import forms
from django.forms import *
from django.template import RequestContext
from accounts.models import User
from django.conf import settings

from django.views.generic.edit import *
from django.core.urlresolvers import *
from django.shortcuts import get_object_or_404, render_to_response, render
from django.http import request

from accounts.forms.user import User_EditForm

@login_required()
def user_edit(request):

    if settings.DEBUG:
        print request.user
        print "User:%s" % request.user.email

    u = User.objects.get(email=request.user.email)

    form = ModelForm(data = request.POST or None, instance=u)

    if request.POST:
        form = User_EditForm(request.POST)
        if form.is_valid():
            form.save()
            if settings.DEBUG:
                print "current record:", u

            return HttpResponseRedirect(reverse('accounts:manage_account'),
                                        RequestContext(request))
    else:
        form = User_EditForm(instance=u)
        if settings.DEBUG:
            print "Not in the post"
        return render_to_response('accounts/useredit.html',
                                  RequestContext(request,
                                                 {'form': form,
                                                  'email': u.email}))



