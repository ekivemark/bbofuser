# -*- coding: utf-8 -*-
"""
bbofuser: apps.v1api.views
FILE: ogets
Created: 9/27/15 7:04 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from oauth2_provider.views.generic import ProtectedResourceView

from django.http import HttpResponse

from apps.v1api.views.patient import get_patient

class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')


    def get_patient(self, request, *args, **kwargs):
        # TODO: get this working
        result = get_patient(request, *args, **kwargs)

        return result
