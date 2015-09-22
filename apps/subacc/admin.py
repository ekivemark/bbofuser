from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Register your models here.
from apps.subacc.models import Device, DeviceAccessLog

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


# DONE: Admin Section for Device AccessLog
class DeviceAccessLogAdmin(admin.ModelAdmin):
    """
    Tailor the Device page in admin module

    """
    # DONE: Admin View for Device Access Log
    list_display = ('device',
                    'account',
                    'action',
                    'accessed',
                    'info',
                    'source',
                    )


admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceAccessLog, DeviceAccessLogAdmin)
