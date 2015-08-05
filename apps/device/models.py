"""
bbofuser:device
FILE: models.py
Created: 8/3/15 4:50 PM

Creating per device authentication

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from uuid import uuid4
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from apps.device.utils import get_phrase

class Device(models.Model):
    """

    Create Per User/Per Device Credentials

    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    device = models.CharField(max_length=40, blank=False)
    account = models.CharField(max_length=250, blank=False)
    password = models.CharField(max_length=40)
    valid_until = models.DateTimeField(default=datetime.now()+timedelta(days=settings.DEFAULT_VALID_UNTIL))
    date_created = models.DateTimeField(auto_now_add=True)
    connected_from = models.CharField(max_length=1000, blank=True)


    def save(self, *args, **kwargs):
        created = self.date_created is None
        if not self.pk or created is None:
            if settings.DEBUG:
                print("Overriding Device save")

            # Assign an account and password with the save
            acc = self.account
            pwd = self.password
            # acc = get_phrase(count=2)
            # pwd = str(uuid4().urn)[9:]
            if settings.DEBUG:
                print("Account:", self.account, "|", acc)
                print("Password:", self.password, "|", pwd)
            # uid4.urn returns string:
            # eg. 'urn:uuid:aec9931c-101b-4803-8666-f047c9159c0c'
            # str()[9:] strips leading "urn:uuid:"

            #self.password = pwd
            #self.account = acc

        super(Device, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s's device:%s" % (self.user.first_name,
                              self.user.last_name,
                              self.device)

    def get_device(self):
        # return the device name
        return self.device

    def get_email(self):
        # Return the email/username
        return self.user_id

