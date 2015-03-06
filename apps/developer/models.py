"""
Models for DeveloperAccount


# Developer
# Organization


"""

from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta
from stdnum.us.itin import is_valid

# Create models here.

# Pre-defined Values
USERTYPE_CHOICES =(('developer','Developer'), ('owner','Account Owner'))


class Developer(models.Model):
    user            = models.OneToOneField(User)
    user_name        = models.CharField(blank = True, max_length=30,
                                       default = "")
    user_type        = models.CharField(max_length=10,
                                           choices = USERTYPE_CHOICES,
                                           default = "developer")
    agree_terms = models.BooleanField(blank=True, default=None)
    terms_agreed_date = models.DateField(blank = True, null = True)
    organization = models.CharField(max_length=100)
    #tin = models.CharField(max_length=12, default="", blank=True)
    #termsVersion = models.CharField(max_length=10)
    #accountManager = models.BooleanField(default=False)

    def __unicode__(self):
        return '[%s]%s %s (%s)' % (self.user_name,
                                   self.user.first_name,
                                   self.user.last_name,
                                   self.user_type)


