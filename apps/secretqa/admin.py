from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Register your models here.
from apps.secretqa.models import QA

# Security Questions and Answers


class QA_Admin(admin.ModelAdmin):
    """
    Tailor the Security QA page in the main Admin module
    """
    # DONE: Add Admin view for SEcurity
    list_display = ('user',
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
                    )


# admin.site.register(Account)
admin.site.register(QA, QA_Admin)
