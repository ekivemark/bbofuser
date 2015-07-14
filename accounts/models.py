"""
Models for DeveloperAccount
Renamed to accounts from developer

# Terms = Agreement
# Developer = Account
# Organization

# Django Registration uses username. To switch to using email requires
# a custom user model. This is defined in settings and needs to be done
# before the first makemigration. ie. blow the database away and start
# again if you make changes later.
# https://docs.djangoproject.com/en/1.8/topics/auth/customizing/#auth-custom-user

# Great documentation on switching to email as username:
# http://blackglasses.me/2013/09/17/custom-django-user-model/


"""
import random
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.auth.models import (
    User, BaseUserManager, AbstractBaseUser)

from django.contrib.auth.signals import user_logged_out
from datetime import date, datetime, timedelta
from django.utils import timezone
from django.utils.timezone import make_aware
from stdnum.us.itin import is_valid

from django.contrib import auth
from django.contrib.auth.models import AbstractBaseUser
from accounts.utils import strip_url, CARRIER_EMAIL_GATEWAY, CARRIER_SELECTION, \
    cell_email, send_sms_pin
from phonenumber_field.modelfields import PhoneNumberField

# Extending Application with OAuth Toolkit
from oauth2_provider.models import AbstractApplication

# Create models here.

# Pre-defined Values
USERTYPE_CHOICES =(('accounts','Developer'), ('owner','Account Owner'))

USER_ROLE_CHOICES = (('primary','Account Owner'),
                     ('backup', 'Backup Owner'),
                     ('member', 'Member'),
                     ('none', 'NONE'),
                     )

class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    site_url = models.URLField(verbose_name="Site Home Page",
                               default="",
                               unique=True,
                               blank=False)
    domain = models.CharField(max_length=254, blank=False,
                              unique=True,
                              default="domain.com"
                              )
    name = models.CharField(max_length=200, blank=True, default="")

    privacy_url = models.URLField(verbose_name="Privacy Terms Page",
                                  default="http://")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='+',
                              blank=True, null=True)
    alternate_owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                                        related_name='+',
                                        blank=True,
                                        null=True)

    def __str__(self):
        #return '%s (%s)' % (self.name,
        #                    self.domain)
        return str(self.domain)

#class Application(models.Model):
#@login_required()
class OrgApplication(AbstractApplication):
    # Application keys
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL,
    #                           related_name='+',
    #                           blank=True,
    #                           null=True,
    #                           )

    organization = models.ForeignKey(Organization,
                                      related_name='+',
                                      blank=True,
                                      null=True,
                                      )
    icon_link = models.URLField(blank=True,
                                null=True,
                                default="")

    def get_absolute_url(self):
        return reverse('accounts:orgapplication_detail', args=[str(self.pk)])


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
    # Done: modify joined to date_joined in user model
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # DONE: Create link to Organization
    # DONE: Create Organization Role
    affiliated_to = models.ForeignKey(Organization,
                                      null=True,
                                      default="",
                                      )
    organization_role = models.CharField(max_length=30,choices=USER_ROLE_CHOICES,
                                         blank=True, default="none")
    # DONE: Add mobile number and carrier
    mobile = PhoneNumberField(blank=True)
    carrier = models.CharField(max_length=100,
                               blank=True,
                               default="None",
                               choices=CARRIER_SELECTION,
                               )
    # DONE: Add switch for Multi-factor Authentication via mobile
    mfa = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name',]

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    #def __str__(self):              # __unicode__ on Python 2
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

    def __str__(self):                      # __unicode__ on Python 2
       #return "%s %s (%s)" % (self.first_name,
        #                       self.last_name,
        #                       self.email)
        return str(self.email)

    def Meta(self):
        verbose_name = _('User')
        verbose_name_plural = _('Users')


class Agreement(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=100,blank = True,
                                   default = "Terms of Use")
    version = models.CharField(max_length=20, blank=True)
    terms_url = models.URLField(verbose_name="Link to Terms",
                                default="http://dev.bbonfhir.com/static/accounts/terms_of_use.html")
    effective_date = models.DateTimeField()

    def __str__(self):
        # format object return python 2.x
        # Use __str__ in python 3.x
        # formats output - useful for admin interface instead of seeing model object
        return '%s:%s (v%s)' % (self.id,
                             self.description,
                             self.version)

    def save(self, *args, **kwargs):
        """
        On save update the Effective_Date
        """
        if not self.id:
                self.effective_date = datetime.today()

        return super(Agreement, self).save(*args, **kwargs)


def alertme(sender, user, request, **kwargs):
    print("USER LOGGED OUT!") #or more sophisticated logging

user_logged_out.connect(alertme)


class ValidSMSCode(models.Model):
    user               = models.ForeignKey(settings.AUTH_USER_MODEL)
    sms_code           = models.CharField(max_length=4, blank=True)
    expires            = models.DateTimeField(default=datetime.now)
    send_outcome       = models.CharField(max_length=250, blank=True)


    def __str__(self):
        return '%s for user %s expires at %s' % (self.sms_code,
                                                 self.user,
                                                 self.expires)

    def save(self, **kwargs):
        up=self.user
        rand_code=random.randint(1000,9999)
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

        if up.mfa:
            new_number = cell_email(up.mobile, up.carrier)
            #send an sms code
            self.send_outcome = send_sms_pin(up.mobile,
                                             new_number,
                                             self.sms_code )
        else:
            self.send_outcome = ''
        super(ValidSMSCode, self).save(**kwargs)
