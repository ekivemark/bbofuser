"""
developeraccount
FILE: organization
Created: 6/25/15 10:48 AM

forms related to Organization

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.shortcuts import render, get_object_or_404
from django import forms
from django.conf import settings

from accounts.models import User, USER_ROLE_CHOICES
from accounts.utils import strip_url

