from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Register your models here.
from apps.device.models import Device

# Device




class DeviceAdmin(admin.ModelAdmin):
    """
    Tailor the Device page in the main Admin module
    """
    # DONE: Add Admin view for Devices
    list_display = ('user',
                    'device',
                    'account',
                    'password',
                    'valid_until',
                    )


# admin.site.register(Account)
admin.site.register(Device, DeviceAdmin)
