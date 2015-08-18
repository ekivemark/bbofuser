from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

# Register your models here.
from accounts.models import (User,
                             ValidSMSCode,
                             Application,
                             Crosswalk)


# TODO: Fix Admin Panels - Bootstrap Layout is not fully functional
# TODO: Add Admin Breadcrumbs?
# TODO: Allow record to be added to empty database

# Account

class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required
    fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput,
                                help_text="<br/>Enter your password again to confirm.")

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name',
                  'is_active', 'is_admin', 'is_staff', 'notify_activity')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name',
                                      'last_name',
                                      'mobile',
                                      'carrier',
                                      'mfa',
                                      'notify_activity')}),
        (
        'Permissions', {'fields': ('is_admin', 'is_active', 'is_staff',)}),
    )

    # TODO: Need to make phone number formatting more user friendly
    # Currently requires +Country code


    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class ApplicationAdmin(admin.ModelAdmin):
    """
    Tailor the Application page in the main Admin module
    """
    # DONE: Add Admin view for applications
    list_display = ('name', 'user')


# admin.site.register(Account)
admin.site.register(User, UserAdmin)
admin.site.register(Application, ApplicationAdmin)
# admin.site.register(ApplicationKey)
admin.site.register(ValidSMSCode)
admin.site.register(Crosswalk)

admin.site.unregister(Group)
