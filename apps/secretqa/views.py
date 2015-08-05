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

from apps.secretqa.models import QA
from apps.secretqa.forms import (QA_EditForm,
                                QA_View, QA_Form)
from apps.device.utils import get_phrase
from datetime import datetime, timedelta


def secretqa_index(request):
    # Show Security Questions Home Page

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print(settings.APPLICATION_TITLE, "in apps.secretqa.views.secretqa_index")

    context = {}
    return render_to_response('secretqa/index.html',
                              RequestContext(request, context, ))


@login_required()
def secretqa_add(request):

    # TODO: Get QA Add Working
    if settings.DEBUG:
        print("In apps.secretqa.views.secretqa_add")

    if request.POST:
        form = QA_EditForm(request.POST)
        if form.is_valid():
            if settings.DEBUG:
                print("Form is valid. Adding Security Questions")

            q = QA()

            q.user = request.user
            q.question_1 = form.cleaned_data['question_1']
            q.answer_1 = form.cleaned_data['answer_1']
            q.question_2 = form.cleaned_data['question_2']
            q.answer_2 = form.cleaned_data['answer_2']
            q.question_3 = form.cleaned_data['question_3']
            q.answer_3 = form.cleaned_data['answer_3']
            q.question_4 = form.cleaned_data['question_4']
            q.answer_4 = form.cleaned_data['answer_4']
            q.question_5 = form.cleaned_data['question_5']
            q.answer_5 = form.cleaned_data['answer_5']

            q.save()

            return HttpResponseRedirect(reverse('accounts:manage_account'),
                                        RequestContext(request))


        else:
            messages.error(request,"Did you provide Security Questions AND answers?")
            return render(request, 'secretqa/secretqa_add.html',
                          {'form': form,
                           })

    else:


        form = QA_EditForm()

    return render(request,
                  'secretqa/secretqa_add.html',
                  {'form': form, }
                  )


@login_required()
def secretqa_edit(request):

    # DONE: Get QA Edit working

    if settings.DEBUG:
        print(request.user)
        print("Entering Security Question Editing with:%s" % request.user)


    q = QA.objects.get(user=request.user)

    if settings.DEBUG:
        print("QA:", q)

    form = QA_EditForm(data=request.POST or None, instance=q)

    if request.POST:
        form = QA_EditForm(request.POST)
        if form.is_valid():

            if settings.DEBUG:
                print("Form is valid - current record:", q)

            # Update Device here

            q.question_1 = form.cleaned_data['question_1']
            q.answer_1 = form.cleaned_data['answer_1']
            q.question_2 = form.cleaned_data['question_2']
            q.answer_2 = form.cleaned_data['answer_2']
            q.question_3 = form.cleaned_data['question_3']
            q.answer_3 = form.cleaned_data['answer_3']
            q.question_4 = form.cleaned_data['question_4']
            q.answer_4 = form.cleaned_data['answer_4']
            q.question_5 = form.cleaned_data['question_5']
            q.answer_5 = form.cleaned_data['answer_5']

            # Update Fields above
            if settings.DEBUG:
                print("Updated to:", q)
            q.save()

            return HttpResponseRedirect(reverse('accounts:manage_account'),
                                        RequestContext(request))
        else:

            if settings.DEBUG:
                print("Form is invalid")

            messages.error(request, "There was an input problem.")
            return render(request, 'secretqa/secretqa_edit.html',
                          {'form': form, 'questions': q })

    else:
        q = QA.objects.get(user=request.user)

        if settings.DEBUG:
            print("in the get with QA:", q, )
        form = QA_EditForm(initial={'question_1':q.question_1,
                                    'answer_1':q.answer_1,
                                    'question_2':q.question_2,
                                    'answer_2':q.answer_2,
                                    'question_3':q.question_3,
                                    'answer_3':q.answer_3,
                                    'question_4':q.question_4,
                                    'answer_4':q.answer_4,
                                    'question_5':q.question_5,
                                    'answer_5':q.answer_5,
                                             })
        if settings.DEBUG:
            print("Not in the post in the get")
        return render(request, 'secretqa/secretqa_edit.html',
                      {'form': form,
                       'questions': q})


@login_required()
def pop_answer(request, qa):
    # pop a modal view with a specific Answer to a Secret Question

    pa = QA.objects.get(user=request.user)

    if settings.DEBUG:
        print("Secret Record:", pa)
        print("Popup Answer:", qa)

    if qa == '1':
        q = pa.get_question_1_display()
        a = pa.answer_1
    elif qa == '2':
        q = pa.get_question_2_display()
        a = pa.answer_2
    elif qa == '3':
        q = pa.question_3
        a = pa.answer_3
    elif qa == '4':
        q = pa.question_4
        a = pa.answer_4
    elif qa == '5':
        q = pa.question_5
        a = pa.answer_5
    else:
        q = "NO QUESTION"
        a = "NO ANSWER"


    modal_form = QA_Form

    return render(request,
                  'secretqa_answer.html',
                  {'pa': pa,
                   'qa': qa,
                   'q': q,
                   'a': a})


