"""
bbofuser:device aka Sub-account
FILE: models.py
Created: 8/3/15 4:50 PM

Creating per device (aka Sub-account) authentication

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from uuid import uuid4
from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone

DAL_ACTION_CHOICES = (('ACCESS', 'Access'),
                      ('PERMISSION','Permission'),
                      ('BLOCKED','No Permission'),
                      ('INACTIVE', 'Inactive'),
                      ('WRONG', 'Wrong Answer Given')
                      )

class Device(models.Model):
    """

    Create Per User/Per Device Credentials

    """
    device       = models.CharField(max_length=40, blank=False,
                                    verbose_name="Sub-Account Nick Name")
    user         = models.ForeignKey(settings.AUTH_USER_MODEL)
    account      = models.CharField(max_length=80, blank=False, verbose_name="User name")
    password     = models.CharField(max_length=40)
    valid_until  = models.DateTimeField(default=datetime.now()+timedelta(days=settings.DEFAULT_VALID_UNTIL))
    date_created = models.DateTimeField(auto_now_add=True)
    connected_from = models.CharField(max_length=1000, blank=True)
    active       = models.BooleanField(default=True)
    deleted      = models.BooleanField(default=False)
    used         = models.BooleanField(default=False, verbose_name="Used to access your Account")
    permitted    = models.BooleanField(default=False, verbose_name="Permission Given")

    def save(self, *args, **kwargs):
        created = self.date_created is None
        if not self.pk or created is None:
            if settings.DEBUG:
                print("Overriding Sub-account save")

            # Assign an account and password with the save
            # DONE: Save as lower case Account and Password
            # DONE: Strip spaces from end of Account and Password
            acc = self.account
            if not acc.lower() == acc:
                self.account = acc.strip().lower()
            pwd = self.password
            if not pwd.lower() == pwd:
                self.password = pwd.strip().lower()
            if settings.DEBUG:
                print("Account:", self.account, "|", acc)
                print("Password:", self.password, "|", pwd)
            # uid4.urn returns string:
            # eg. 'urn:uuid:aec9931c-101b-4803-8666-f047c9159c0c'
            # str()[9:] strips leading "urn:uuid:"

        super(Device, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s's Sub-account:%s" % (self.user.first_name,
                              self.user.last_name,
                              self.device)

    def get_device(self):
        # DONE: return the Sub-account name
        return self.device

    def get_subaccount(self):
        # DONE: return the sub-account Name
        return self.device

    def get_email(self):
        # Return the email/username
        return self.user_id

    def get_account(self):
        # Return the account
        return self.account

    def is_deleted(self):
        # DONE: Get deleted state
        # Return the Deleted State (Devices/Sub-accounts are marked
        # deleted and not removed to ensure accounts are unique
        # and not re-used by another user
        return self.deleted

    def is_active(self):
        # DONE: Return the Active State
        result = False
        if not self.deleted:
            if self.active:
                result = True
        else:
            result = False

        return result

    def is_used(self):
        # DONE: Return whether Device has been logged in
        result = False
        if self.used:
            result = True
        return result

    def set_used(self):
        # DONE: Return whether Device has been logged in
        result = False
        if not self.used:
            self.used = True
            super(Device, self).save()
            result = True
        return result

    def is_permitted(self):
        # DONE: Add check for Device is permitted to access
        result = False
        if self.permitted:
            result = True
        return result

    def is_authorized(self):
        # Check all controls for allowed access
        result = {'result': False,
                  'message': ""}
        if self.deleted:
            result['result'] = False
            result['message'] = "Failed - DELETED Sub-Account"
            if settings.DEBUG:
                print(result)
            return result
        if not self.active:
            result['result'] = False
            result['message'] = "Failed - INACTIVE Sub-account"
            if settings.DEBUG:
                print(result)
            return result
        if self.valid_until <= timezone.now():
            result['result'] = False
            result['message'] = "Failed - VALID UNTIL PERIOD ENDED"
            if settings.DEBUG:
                print(result)
            return result
        if not self.permitted:
            result['result'] = False
            result['message'] = "Failed - NOT PERMITTED"
            if settings.DEBUG:
                print(result)
            return result
        result = {}
        return result


# DONE: Add DeviceAccessLog
# DONE: Add IP Address of client
class DeviceAccessLog(models.Model):
    """
    Add Entry for each Login by Device
    Device Key
    Record Date and Time

    """
    device      = models.ForeignKey(Device)
    account     = models.CharField(max_length=80)
    action      = models.CharField(max_length=10,
                                   choices=DAL_ACTION_CHOICES,
                                   default="ACCESS")
    accessed    = models.DateTimeField(auto_now_add=True)
    info        = models.CharField(max_length=200, blank=True, )
    source      = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return "%s using %s" % (self.device,
                                self.account)
