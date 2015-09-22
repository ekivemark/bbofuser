"""
bbofuser:device
FILE: views
Created: 8/3/15 6:54 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

import random
from collections import OrderedDict

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
from apps.subacc.utils import get_phrase
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

    # DONE: Get QA Add Working
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


def Get_Question(request, user):
    """
    Pick a question
    :param user:
    :return: string with question
    """

    if settings.DEBUG:
        print("Entering apps.secretqa.views.Get_Question")
    # Use user to find QA entry
    qa = QA.objects.get(user=user)

    if settings.DEBUG:
        print("Questions:", qa)

    # setup dict
    a = []
    q = []

    # mdl = qa._meta.get_all_field_names()
    # print("QA Model:", mdl)

    # Cycle through questions in record
    # If Answer then add to OrderedDict()
    for x in range(1, 6):
        q_var = "question_" + str(x)
        a_var = "answer_" + str(x)
        if settings.DEBUG:
            print("Q",str(x),"|",
                  q_var,
                  ":",
                  getattr(qa, q_var),
                  "|",
                  a_var,
                  ":",
                  getattr(qa, a_var))

        if getattr(qa, a_var):
            a.append([a_var,getattr(qa, a_var)])
            if x > 2:
                q.append([q_var, getattr(qa, q_var)])
                if settings.DEBUG:
                    print("Question:", getattr(qa, q_var))
            else:
                q_text = dict(settings.SECURITY_QUESTION_CHOICES).get(getattr(qa, q_var))
                if settings.DEBUG:
                    print("Question(lookup):", q_text)
                q.append([q_var, q_text])

    n = random.randint(0, len(q)-1)
    # Pick a Random Question from the list with answers
    if settings.DEBUG:
        print("Answered Questions:", q)
        print("With Answers:", a)
        print("Choosing:", n)
        print("q:",len(q))

    picked_q = q[n]
    picked_a = a[n]

    if settings.DEBUG:
        print("Picked Q:", picked_q)
        print("Answer:", picked_a)

    return picked_q

def Check_Answer(user, question, answer):
    """
    Check the User Answer for the Question against the Answer.
    Push both Answer and response to lower()
    :param user:
    :param question:
    :param answer:
    :return:
    """

    Sec_Qn_result = False
    qa =     qa = QA.objects.get(user=user)

    # setup dict
    a = []
    q = []

    for x in range(1, 6):
        q_var = "question_" + str(x)
        a_var = "answer_" + str(x)

        if getattr(qa, a_var):
            if x < 3:
                q_text = dict(settings.SECURITY_QUESTION_CHOICES).get(getattr(qa, q_var))
            else:
                q_text = getattr(qa, q_var)
            if settings.DEBUG:
                print("Checking", q_text,
                      " against/nQuestion asked:", question )
            q.append([q_var, q_text])
            if q_text == question:
                # Check the Answer
                a_text = getattr(qa, a_var).lower()
                if answer.lower() == a_text:
                    Sec_Qn_result = True
                    if settings.DEBUG:
                        print("RIGHT Answer/n",
                              answer.lower(),
                              " = ",
                              a_text)
                    return Sec_Qn_result
                else:
                    Sec_Qn_result = False
                    if settings.DEBUG:
                        print("Wrong Answer/n",
                              answer.lower(),
                              " != ",
                              a_text)
                    return Sec_Qn_result

    if settings.DEBUG:
        print("No match on question:", question,
              "/nin", q )
    return Sec_Qn_result