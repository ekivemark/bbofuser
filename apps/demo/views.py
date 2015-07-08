# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import default_storage

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models.fields.files import FieldFile
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.contrib import messages

# used by DemoApi
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
import requests
import json
import dicttoxml
from xml.dom.minidom import parseString

from .forms import ContactForm, FilesForm, ContactFormSet


# http://yuji.wordpress.com/2013/01/30/django-form-field-in-initial-data-requires-a-fieldfile-instance/
class FakeField(object):
    storage = default_storage


fieldfile = FieldFile(None, FakeField, 'dummy.txt')


class HomePageView(TemplateView):
    template_name = 'demo/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.info(self.request, 'This is a demo of a message.')
        return context


class DefaultFormsetView(FormView):
    template_name = 'demo/formset.html'
    form_class = ContactFormSet


class DefaultFormView(FormView):
    template_name = 'demo/form.html'
    form_class = ContactForm


class DefaultFormByFieldView(FormView):
    template_name = 'demo/form_by_field.html'
    form_class = ContactForm


class FormHorizontalView(FormView):
    template_name = 'demo/form_horizontal.html'
    form_class = ContactForm


class FormInlineView(FormView):
    template_name = 'demo/form_inline.html'
    form_class = ContactForm


class FormWithFilesView(FormView):
    template_name = 'demo/form_with_files.html'
    form_class = FilesForm

    def get_context_data(self, **kwargs):
        context = super(FormWithFilesView, self).get_context_data(**kwargs)
        context['layout'] = self.request.GET.get('layout', 'vertical')
        return context

    def get_initial(self):
        return {
            'file4': fieldfile,
        }

class PaginationView(TemplateView):
    template_name = 'demo/pagination.html'

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        lines = []
        for i in range(10000):
            lines.append('Line %s' % (i + 1))
        paginator = Paginator(lines, 10)
        page = self.request.GET.get('page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context['lines'] = show_lines
        return context


class MiscView(TemplateView):
    template_name = 'demo/misc.html'


def DemoApi(request):

    # Demo API
    application_title = settings.APPLICATION_TITLE
    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print(application_title, "in demo.views.DemoApi")

    fhir_server_url = "http://localhost:8080/fhir-p/"
    fhir_server_param = "baseDstu2/Patient/1/$everything?_format=json"

    data = json.dumps({})
    r = requests.get(fhir_server_url+fhir_server_param, )


    #print(r.json)
    #print(r.content)

    result = r.content
    result_content = json.loads(r.content)
    #result = result["resource"]
    result = json.dumps(result_content, indent=4, )
    xmlresult = dicttoxml.dicttoxml(result_content)

    dom = parseString(xmlresult)
    #print(dom.toprettyxml())

    context = {"APPLICATION_TITLE": application_title,"result": result, "xmlresult": dom.toprettyxml(),
               "url": fhir_server_url, "params": fhir_server_param }
    return render_to_response('demo/demoapi.html', RequestContext(request, context))

