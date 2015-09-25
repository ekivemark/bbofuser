"""
Models for bbonfhir Users

# Terms = Agreement
# Developer = Account


# Django Registration uses username. To switch to using email requires
# a custom user model. This is defined in settings and needs to be done
# before the first makemigration. ie. blow the database away and start
# again if you make changes later.
# https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#auth-custom-user

# Great documentation on switching to email as username:
# http://blackglasses.me/2013/09/17/custom-django-user-model/


"""
import collections
import random

from datetime import datetime, timedelta
from uuid import uuid4

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import (User,
                                        BaseUserManager,
                                        AbstractBaseUser)
from django.contrib.auth.signals import user_logged_out
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser
from jsonfield import JSONField
from phonenumber_field.modelfields import PhoneNumberField

from accounts.utils import CARRIER_SELECTION, cell_email, send_sms_pin

# Extending Application with OAuth Toolkit
from oauth2_provider.models import AbstractApplication

# Create models here.

# Pre-defined Values

USERTYPE_CHOICES = (('owner', 'Account Owner'))

USER_ROLE_CHOICES = (('primary', 'Account Owner'),
                     ('backup', 'Backup Owner'),
                     ('none', 'NONE'),
                     )

# DONE: Add Activity Notification Choices
ACTIVITY_NOTIFY_CHOICES = (('N', "No Notifications"),
                           ('E', "Email Message"),
                           ('T', "Text Message")
                           )

# class Application(models.Model):
# @login_required()
class Application(AbstractApplication):
    # Application keys
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                           related_name='+',
    #                           blank=True,
    #                           null=True,
    #                           )

    valid_until = models.DateTimeField(editable=False)
    # editable=False to hide in admin

    def save(self):
        d = timedelta(days=365)

        # only add 365 days if it's the first time the model is saved
        if not self.id:
            self.mydate = datetime.now() + d
            super(MyModel, self).save()

    def get_absolute_url(self):
        return reverse('accounts:application_detail', args=[str(self.pk)])


class UserManager(BaseUserManager):
    def create_user(self,
                    email,
                    first_name,
                    last_name,
                    password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have a unique email address')

        email = self.normalize_email(email)

        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name,
                         password, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email,
                                password=password,
                                first_name=first_name,
                                last_name=last_name,
                                **extra_fields
                                )
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        if settings.DEBUG == True:
            print("%s, active=%s,admin=%s, %s" % (user.email,
                                                  user.is_active,
                                                  user.is_admin,
                                                  user.password))
        return user


class User(AbstractBaseUser):
    """
    Replacing the base user model - switch to using email as username
    """
    email = models.EmailField(verbose_name='email address',
                              max_length=255,
                              unique=True,
                              db_index=True)
    first_name = models.CharField(max_length=50,
                                  blank=True)
    last_name = models.CharField(max_length=50,
                                 blank=True)
    medicare_connected = models.BooleanField(default=False)
    medicare_verified = models.BooleanField(default=False)
    # Done: modify joined to date_joined in user model
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # DONE: Add Activity Notification
    notify_activity = models.CharField(max_length=1,
                                       default="N",
                                       choices=ACTIVITY_NOTIFY_CHOICES,
                                       verbose_name="Notify Account Activity")

    # DONE: Add mobile number and carrier
    mobile = PhoneNumberField(blank=True)
    carrier = models.CharField(max_length=100,
                               blank=True,
                               default="None",
                               choices=CARRIER_SELECTION,
                               )
    # DONE: Add switch for Multi-factor Authentication via mobile
    mfa = models.BooleanField(default=False,
                              verbose_name='Send Login PIN Code?')
    verified_mobile = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    # def __str__(self):              # __unicode__ on Python 2
    #    return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    # @property
    # def is_staff(self):
    #     "Is the user a member of staff?"
    #     # Simplest possible answer: All admins are staff
    #     return self.is_admin

    def __str__(self):  # __unicode__ on Python 2
        # return "%s %s (%s)" % (self.first_name,
        #                       self.last_name,
        #                       self.email)
        return str(self.email)

    def Meta(self):
        verbose_name = _('User')
        verbose_name_plural = _('Users')


def alertme(sender, user, request, **kwargs):
    print("USER LOGGED OUT!")  # or more sophisticated logging


user_logged_out.connect(alertme)


class ValidSMSCode(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    sms_code = models.CharField(max_length=4, blank=True)
    expires = models.DateTimeField(default=datetime.now)
    send_outcome = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return '%s for user %s expires at %s' % (self.sms_code,
                                                 self.user,
                                                 self.expires)

    def save(self, **kwargs):
        up = self.user
        rand_code = random.randint(1000, 9999)
        if not self.sms_code:
            if up.mobile != '+19999999999':
                self.sms_code = rand_code
            else:
                self.sms_code = '9999'
            if settings.DEBUG:
                print(self.sms_code)

        now = timezone.now()
        expires = now + timedelta(minutes=settings.SMS_LOGIN_TIMEOUT_MIN)
        self.expires = expires

        # Removing mfa check.
        # Only call ValidSMSCode is user.MFA is true or Verifying phone
        phone_email = cell_email(up.mobile, up.carrier)
        # send an sms code
        self.send_outcome = send_sms_pin(phone_email,
                                         self.sms_code)

        super(ValidSMSCode, self).save(**kwargs)


class Crosswalk(models.Model):
    """

    HICN to UUID Crosswalk and back.
    Linked to User Account

    """
# TODO: Implement PyCrypto to encrypt HICN

    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    guid = models.CharField(max_length=40)
    hicn = models.CharField(max_length=40, blank=True)
    mmg_user = models.CharField(max_length=250, blank=True)
    mmg_pwd = models.CharField(max_length=16, blank=True)
    mmg_name = models.CharField(max_length=250, blank=True)
    mmg_email = models.EmailField(max_length=250, blank=True, null=True)
    mmg_account = models.TextField(blank=True)
    mmg_bbdata = models.TextField(blank=True)
    mmg_bbjson = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict},
                           blank=True)
    mmg_bbfhir = models.BooleanField(default=False)
    fhir = models.CharField(max_length=40, blank=True )
    fhir_url_id = models.CharField(max_length=80, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    # FHIR = Identifier contained in the Patient Profile
    # fhir_url_id = Identifier used in the patient Profile URL
    # eg. /baseDstu2/Patient/{id}
    # This will allow us to construct a URL to make a call directly to
    # a record, rather than requiring a search

    # MyMedicare.gov Password Creation Guidelines
    # Must be 8 to 16 characters long
    # Must contain at least one letter
    # Must contain at least one number
    # May also contain one or more of the following special characters:
    # @ ! $ % ^ * ( )
    # Must be different from the previous six (6) passwords
    # Cannot be the same as your Username
    # Cannot contain your Medicare Number or SSN

    def save(self, *args, **kwargs):
        created = self.date_created is None
        if not self.pk or created is None:
            if settings.DEBUG:
                print("Overriding Crosswalk save")

            # Assign a GUID with the save
            uid = str(uuid4().urn)[9:]
            # uid4.urn returns string:
            # eg. 'urn:uuid:aec9931c-101b-4803-8666-f047c9159c0c'
            # str()[9:] strips leading "urn:uuid:"
            self.guid = uid

        super(Crosswalk, self).save(*args, **kwargs)

    def __str__(self):
        return "%s %s[%s]" % (self.user.first_name,
                              self.user.last_name,
                              self.guid)

    def get_guid(self):
        # return the uuid
        return self.guid

    def get_email(self):
        # Return the email/username
        return self.user_id

    def get_fhir(self):
        # Return the FHIR Identifier
        return self.fhir

    def get_fhir_url_id(self):
        # Return the patient profile id to add to url
        return self.fhir_url_id

