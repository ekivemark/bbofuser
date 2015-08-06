"""
bbofuser:secretqa
FILE: forms
Created: 8/3/15 6:46 PM

Secret Questions and Answers for User Account Security

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.shortcuts import render, get_object_or_404
from django import forms
from django.forms import (HiddenInput, Textarea)
from django.conf import settings

from apps.secretqa.models import QA


def QA_View(request, mymodel_id):
    class MyModelForm(forms.ModelForm):
        class Meta:
            model = QA

    model = get_object_or_404(QA, pk=mymodel_id)
    form = MyModelForm(instance=model)
    return render(request, 'securityqa/model.html', {'form': form})

class QA_Form(forms.ModelForm):
    class Meta:
        model = QA
        fields = ['user',
                  'question_1',
                  'answer_1',
                  'question_2',
                  'answer_2',
                  'question_3',
                  'answer_3',
                  'question_4',
                  'answer_4',
                  'question_5',
                  'answer_5',
                  ]

        def __init__(self, *args, **kwargs):
            super(QA_Form, self).__init__(*args, **kwargs)
            self.helper = FormHelper(self)
            self.helper.layout.append(Submit('submit', 'Submit'))


class QA_EditForm(forms.ModelForm):


    question_1 = forms.CharField(max_length=2,
                                 widget=forms.Select(choices=settings.SECURITY_QUESTION_CHOICES))
    answer_1   = forms.CharField(max_length=80,)
    question_2 = forms.CharField(max_length=2,
                                 widget=forms.Select(choices=settings.SECURITY_QUESTION_CHOICES))
    answer_2   = forms.CharField(max_length=80,)
    question_3 = forms.CharField(max_length=80, required=False)
    answer_3   = forms.CharField(max_length=80, required=False)
    question_4 = forms.CharField(max_length=80, required=False)
    answer_4   = forms.CharField(max_length=80, required=False)
    question_5 = forms.CharField(max_length=80, required=False)
    answer_5   = forms.CharField(max_length=80, required=False)


    class Meta:
        model = QA
        fields = ('question_1',
                  'answer_1',
                  'question_2',
                  'answer_2',
                  'question_3',
                  'answer_3',
                  'question_4',
                  'answer_4',
                  'question_5',
                  'answer_5',
                  )

    def clean(self):
        error_messages = []
        if self.cleaned_data.get('question_1') and not self.cleaned_data.get('answer_1'):
            error_messages.append(
                "You didn't provide an Answer to Question 1"
            )
        if self.cleaned_data.get('question_2') and not self.cleaned_data.get('answer_2'):
            error_messages.append(
                "You didn't provide an Answer to Question 2"
            )
        if self.cleaned_data.get('question_3') and not self.cleaned_data.get('answer_3'):
            error_messages.append(
                "You didn't provide an Answer to Question 3"
            )
        if self.cleaned_data.get('question_4') and not self.cleaned_data.get('answer_4'):
            error_messages.append(
                "You didn't provide an Answer to Question 4"
            )
        if self.cleaned_data.get('question_5') and not self.cleaned_data.get('answer_5'):
            error_messages.append(
                "You didn't provide an Answer to Question 5"
            )

        if len(error_messages):
            raise forms.ValidationError(' & '.join(error_messages))

        return self.cleaned_data

