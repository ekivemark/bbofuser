"""
bbofuser:device
FILE: views
Created: 8/3/15 6:54 PM

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from datetime import datetime, timedelta
from uuid import uuid4

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import (get_user_model,
                                 login as django_login,
                                 authenticate as django_authenticate,
                                 logout as django_logout)
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import (reverse,
                                      reverse_lazy)
from django.http import HttpResponseRedirect
from django.shortcuts import (render,
                              render_to_response,
                              redirect)
from django.template import RequestContext
from django.utils import timezone

from accounts.decorators import session_master
from accounts.models import User
from accounts.utils import (send_activity_message,
                            cell_email,
                            email_mask)
from apps.device.models import (Device,
                                DeviceAccessLog)
from apps.device.forms import (Device_AuthenticationForm,
                               Device_EditForm,
                               Device_AddForm,
                               Device_View,
                               unique_account)
from apps.device.utils import (get_phrase,
                               session_device,
                               via_device,
                               Master_Account,
                               Device_Set_To_Permitted)

from apps.secretqa.views import (Get_Question,
                                 Check_Answer)
from apps.device.forms import Question_Form


@session_master
@login_required
def device_index(request):
    # Show Device Home Page

    DEBUG = settings.DEBUG_SETTINGS

    if DEBUG:
        print(settings.APPLICATION_TITLE, "in apps.device.views.device_index")

    context = {}
    return render_to_response('device/index.html',
                              RequestContext(request, context, ))


@session_master
@login_required
def device_add(request):

    if settings.DEBUG:
        print("In apps.device.views.device_add")

    if request.POST:
        form = Device_AddForm(request.POST)
        if form.is_valid():
            if settings.DEBUG:
                print("Form is valid. Adding Device")

            d = Device()

            # DONE: Force Account and password to Lower Case
            d.user = request.user
            d.password = form.cleaned_data['password'].strip().lower()
            d.device = form.cleaned_data['device']
            # account needs to be unique
            d.account = form.cleaned_data['account'].strip().lower()
            d.valid_until = form.cleaned_data['valid_until']

            d.save()

            return HttpResponseRedirect(reverse('accounts:manage_account'),
                                        RequestContext(request))
        else:
            messages.error(request,"Did you use a device name?")
            return render(request, 'device/device_add.html',
                          {'form': form,
                           })
    else:
        acc = get_phrase(count=2)
        pwd = str(uuid4().urn)[9:]
        until_date = datetime.now()+timedelta(days=settings.DEFAULT_VALID_UNTIL)
        if settings.DEBUG:
            print("Account:",acc)
            print("Password:", pwd)

        form = Device_EditForm(initial={'account':acc,
                                        'password':pwd,
                                        'valid_until': until_date})



    return render(request,
                  'device/device_add.html',
                  {'form': form,
                   'password': pwd, }
                  )


@session_master
@login_required
def device_edit(request, pk):
    if settings.DEBUG:
        print(request.user)
        print("Entering Device Edit with:%s" % pk)

    d = Device.objects.get(pk=pk)

    if settings.DEBUG:
        print("Device", d)

    form = Device_EditForm(data=request.POST or None, instance=d)

    if request.POST:
        form = Device_EditForm(request.POST)
        if form.is_valid():
            if d.account != form.cleaned_data['account']:
                if not unique_account(form.cleaned_data['account']):

                    messages.error(request,"Account Name changed and is NOT Unique")
                    return render(request, 'device/device_edit.html',
                          {'form': form, 'device': d.device, })

            if settings.DEBUG:
                print("Form is valid - current record:", d)

            # Update Device here

            # DONE: Force Account and password to Lower Case
            d.device = form.cleaned_data['device']
            d.account = form.cleaned_data['account'].strip().lower()
            d.password = form.cleaned_data['password'].strip().lower()
            d.valid_until = form.cleaned_data['valid_until']

            # Update Fields above
            if settings.DEBUG:
                print("Updated to:", d)
            d.save()

            return HttpResponseRedirect(reverse('accounts:manage_account'),
                                        RequestContext(request))
        else:

            if settings.DEBUG:
                print("Form is invalid")

            messages.error(request, "There was an input problem.")
            return render(request, 'device/device_edit.html',
                          {'form': form, 'device': d.device, })

    else:
        d = Device.objects.get(pk=pk)

        if settings.DEBUG:
            print("in the get with Device:", d.device, )
        form = Device_EditForm(initial={'device': d.device,
                                        'account': d.account,
                                        'password': d.password,
                                        'valid_until': d.valid_until,
                                        'used': d.used,
                                        'permitted': d.permitted,
                                             })
        if settings.DEBUG:
            print("Not in the post in the get")
        return render(request, 'device/device_edit.html',
                      {'form': form,
                       'device': d})

@session_master
@login_required
def Device_Delete(request, pk):
    """
    We will not delete. Instead we will flag as deleted.
    This will avoid user accounts being reused
    """
    if settings.DEBUG:
        print("in apps.device.views.Device_Delete")
        print("Device:", pk,)

    d = Device.objects.get(pk=pk)

    if request.POST:
        form = Device_EditForm()
        if form.is_valid:
            if settings.DEBUG:
                print("in the POST")
            d.deleted = True
            d.save()
            return HttpResponseRedirect(reverse('accounts:manage_account'),
                                        RequestContext(request))

        else:
            if settings.DEBUG:
                print("Form is invalid")

            messages.error(request, "There was an input problem.")
            return render(request, 'device/device_confirm_delete.html',
                          {'form': form, 'device': d.device, })
    else:
        d = Device.objects.get(pk=pk)
        if settings.DEBUG:
            print("in the get with Device Deletion:", pk)
        form =Device_EditForm()

    return render(request, 'device/device_confirm_delete.html',
                    {'form': form,
                     'device': d})


def device_authenticate(account, password):
    """
    Check for Device Login
    """
    result = None

    try:
        D = Device.objects.get(account=account,
                           password=password,
            # DONE: Ignore Deleted Devices
            # DONE: We check for an active device later
                           active=True,
                           deleted=False)
        if settings.DEBUG:
            print("Matched:", account,"=", D.account)
            print("Pwd Match:", password, "=", D.password)
            print("Active:", D.is_active(), " Deleted:", D.is_deleted())
        result = D
    except Device.DoesNotExist:
        if settings.DEBUG:
            print("account", account, " Password:", password)
            print("device_authenticate: Device.DoesNotExist")
        result = None

    if settings.DEBUG:
        print("Result:", result)
    return result


# DONE: View for Device Permission from User
# DONE: Get Secret Question
# DONE: test answer aqinst secret answer
def ask_user_for_permission(request):
    """

    :param request:
    :param user:
    :param device:
    :return:
    """
    if 'device_ask_permission' in request.session:
        ask_count = int(request.session['device_ask_permission']['count'])
    else:
        ask_count = 0
    ask_count += 1

    if 'device_permission' in request.session:
        device_id = request.session['device_permission']['device']
        user_email   = request.session['device_permission']['user']
        if settings.DEBUG:
            print("User:  ", user_email)
            print("Device:", device_id)
            print("Ask Count:", ask_count)

        user = get_user_model().objects.get(email=user_email)
        device = Device.objects.get(pk=device_id)

    else:
        if settings.DEBUG:
            print("Not passed from Device Login correctly")
        messages.error(request, "Unable to Check Permission")
        return HttpResponseRedirect(reverse("api:home"))

    # Check the number of attempts to get permission
    # DONE: Check ask_permission count against settings.
    if settings.DEVICE_PERMISSION_COUNT:
        max_count = settings.DEVICE_PERMISSION_COUNT
    else:
        # Set a default
        max_count = 3

    if max_count > 0:
        # We need to check the number of attempts
        if ask_count > max_count:
            # Set device as used
            # set message
            # return to api:home
            device.set_used()
            # now we can clear down the count
            request.session['device_ask_permission'] = {}

            messages.error(request, "Too many permission attempts. This device is locked. The account owner will need to reset this device account")
            return HttpResponseRedirect(reverse("api:home"))

    # Now to Ask for Permission

    if settings.DEBUG:
        print("Entering apps.device.views.Ask_User_For_Permission")
        print("request.user:", request.user)
        print("request.session:", request.session)

        print("user passed via session:", user )
        print("device passed via session:", device)

    # We need to work out the user and device
    # should be able to use request.session
    # DONE: Create Ask User For Permission
    # DONE: Create Form and View to get permission
    # DONE: Add view to urls.py
    if request.POST:
        form = Question_Form(request.POST)
        if form.is_valid():
            if Check_Answer(user, form.cleaned_data['question'], form.cleaned_data['answer']):
                # True is good. False is BAD
                # Finish the login process
                # Also have to set device.permitted to True
                permitted_result = Device_Set_To_Permitted(device)
                # DONE: Set device.used = True
                used_result = device.set_used()
                if settings.DEBUG:
                    print("device is now permitted?:", permitted_result)
                    print("device in set to used:", used_result)
                User_Model = get_user_model()
                user = User_Model.objects.get(email=device.user)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                # fix for user.backend attribute

                if settings.DEBUG:
                    print("User_Model:", User_Model)
                    print("user:", user)

                # DONE: Add Email Notification of Permission Given
                if user.notify_activity in "ET":
                    # msg = PERM_MSG0 + user.email + PERM_MSG1 + device.device + PERM_MSG2
                    subject = "Device Connected to " + settings.APPLICATION_TITLE
                    if user.notify_activity in "ET":
                        send_activity_message(request,
                                              user,
                                              subject,
                                              template="accounts/messages/device_permission_email",
                                              context={'device':device.device,
                                                       'email_mask':email_mask(user.email)},
                                              )
              # Otherwise don't send a message

                django_login(request, user)
                session_set = session_device(request, device.device)
                # DONE: Record Access in DeviceAccessLog

                dal_result = Post_Device_Access(request, device, action="PERMISSION")
                if settings.DEBUG:
                    print("Post to Device Access Log:", dal_result)

                # CLEAR DOWN THE REQUEST.SESSION VARIABLE
                request.session['device_permission'] = {}
                request.session['device_ask_permission'] = {}
                if settings.DEBUG:
                    print("User:", user)
                    print("Sessions:", request.session )

                return HttpResponseRedirect(reverse("api:home"))
            else:
                # Failed - Go back to Login
                messages.error(request, "Sorry - that was the wrong answer")
                Post_Device_Access(request, device, action="WRONG")
                # DONE: increment counter in request.session
                request.session['device_ask_permission'] = {'count': ask_count}

                # DONE: Record Access in DeviceAccessLog
                return HttpResponseRedirect(reverse('device:device_login'))
        else:
            messages.error(request,"I am sorry = there was a problem")
            render(request,
                  'device/device_permission.html',
                   {'form': form,
                    'question': form['question']})
    else:

        print("In the GET - about to render question form")

    question = Get_Question(request, user)
    print("Got from Get_Question:",question[1])
    form = Question_Form(initial={'question': question[1]})

    if settings.DEBUG:
        print("Question to ask:", question)
    return render(request,
                  'device/device_permission.html',
                   {'form': form,
                    'question': question,
                    'device': device},
                    )



# DONE: Post Device Access Record
def Post_Device_Access(request, device, action="ACCESS"):
    """

    Add the record of a device access to the DeviceAccessLog
    update Device.Connected_From

    :param device:
    :return:
    """

    # DONE: Get Device Access Log Aging limit
    # DONE: Query DAL for entries older than settings.DEVICE_ACCESS_LOG_DAYS
    if not settings.DEVICE_ACCESS_LOG_DAYS:
        oldest_days = 365
    else:
        oldest_days = settings.DEVICE_ACCESS_LOG_DAYS
    # DONE: Delete entries older than CurrentTime = DEVICE_ACCESS_LOG_DAYS
    to_be_deleted_date = timezone.now() - timedelta(days=oldest_days)
    print("date to delete before:", to_be_deleted_date)

    log = DeviceAccessLog.objects.filter(device=device,accessed__lte=to_be_deleted_date)
    if settings.DEBUG:
        print("Device:", device)
        print("Records to be Deleted from Log:", log.count())

    if log.count()>0:
        log.delete()

    if settings.DEBUG:
        print("Device:", device)
        print("Records Deleted from Log:", log.count())

    DAL = DeviceAccessLog()

    DAL.device  = device
    DAL.account = device.account
    DAL.action  = action

    if settings.DEBUG:
        print("Log action:", action)
        print("User Agent:", request.META.get('HTTP_USER_AGENT', ''))
        print(len(request.META.get('HTTP_USER_AGENT', '')), " characters")

    DAL.info    = request.META.get('HTTP_USER_AGENT', '')
    DAL.source  = request.META.get('HTTP_X_FORWARDED_FOR’,''') or request.META.get('REMOTE_ADDR')

    result = DAL.save()

    # DONE: Update Device used field.
    # device.used = True
    device.connected_from = DAL.source
    device.save()

    return result


# DONE: Give Device Permission
# def Give_Device_Permission(request, user, device,):
#     """
#     Ask for Device Permission
#     Ask a Security Question
#     Check Security Answer
#     If Passed security then ask for permission
#
#     If permission is denied then set Device.active to false
#         Return False
#     :param device:
#     :return:
#     """
#     result = False
#     if settings.DEBUG:
#         print("Entering apps.device.views.Give_Device_Permission")
#
#     check = device.is_authorized()
#     # is active, is not deleted, is permitted. is valid_until.
#     if not 'result' in check:
#         # No warnings sent bck from is_authorized
#         if settings.DEBUG:
#             print("Check result:", check)
#         return True
#
#     # There was an issue with is_authorized()
#     if not device.used:
#         if not device.permitted:
#             # Device has not been used and we need to check permission
#             # DONE: check permission if device is not used before
#             # We need to Ask Permission and use a challenge question
#             #permission_result = Ask_User_For_Permission(request,
#             #                                            user,
#             #                                            device)
#
#             # Call the ask_permission Screen
#             if settings.DEBUG:
#                 print("About to ask Permission")
#             return HttpResponseRedirect(reverse("device:ask_permission"))
#
#         else:
#             if settings.DEBUG:
#                 print("Device Used:", device.used,
#                       " Permitted:", device.permitted)
#             # Device is permitted
#             return True
#
#     else: # Device has been used
#         if 'result' in check:
#             if settings.DEBUG:
#                 print("Authorized Result", check['result'],":", check['message'])
#                 # Failed authorization checks
#                 # So check if permitted
#             return False
#         else:
#             if settings.DEBUG:
#                 print("Check:", check)
#                 # Authorized Check is empty - so there were no problems
#             return True
#
#
def Device_Login(request, *args, **kwargs):
    """
    Device Login
    :param request:
    :param args:
    :param kwargs:
    :return:
    """

    if request.method == 'POST':
        form = Device_AuthenticationForm(request.POST)
        if settings.DEBUG:
            print("in apps.device.views.Device_Login POST")
        if form.is_valid():
            if settings.DEBUG:
                print("Form is Valid: Authenticating Device")

            # DONE: Remove trailing spaces
            account = form.cleaned_data['account'].strip()
            Dpassword = form.cleaned_data['password'].strip()

            device = device_authenticate(account=account,
                                         password=Dpassword,)
            # device_authenticate will check for active and not deleted
            if settings.DEBUG:
                print("device:", device,)
            permission_check = False
            if device is not None:
                if device.is_active:
                    if settings.DEBUG:
                        print("Active Device:", device.is_active())
                        print("Request.user:", request.user)
                        print("Device.user:", device.user)
                        print("Device used:", device.is_used())
                    # Now get the User Account
                    User_Model = get_user_model()
                    user = User_Model.objects.get(email=device.user)
                    # fix for user.backend attribute
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth_rslt = django_authenticate(username=user.email,
                                                    password=user.password)
                    # DONE: Check for not device.used

                    if not device.used:
                        if not device.permitted:
                            # Device has not been used and we need to check permission
                            # DONE: check permission if device is not used before
                            # We need to Ask Permission and use a challenge question
                            # Call the ask_permission Screen
                            if settings.DEBUG:
                                print("About to ask Permission")
                            form = Question_Form()
                            args = {}
                            args['form']   = form
                            args['user']   = user.email
                            args['device'] = device.id

                            request.session['device_permission'] = {'device':device.id,
                                                                    'user':device.user.email}
                            return HttpResponseRedirect(reverse("device:ask_permission"), args)

                        else: # device.permitted

                            permission_check = True
                            if settings.DEBUG:
                                print("Device Used:", device.used,
                                      " Permitted:", device.permitted)
                                # Device is permitted
                    else: # Device has been used
                        if not device.permitted:
                            if settings.DEBUG:
                                print("Device Used and Device_Permitted NOT Set")
                                # Failed authorization checks
                                # So check if permitted
                            permission_check = False
                            messages.error(request, "You are not permitted access with this account")
                            Post_Device_Access(request, device, action="NOTPERMITD")
                            # DONE: Record Access in DeviceAccessLog

                            return HttpResponseRedirect(reverse("api:home"))
                        else:
                            if settings.DEBUG:
                                print("Device Used:", device.used,
                                      " Permitted:", device.permitted)
                                # Authorized Check is empty - so there were no problems
                            permission_check = True
                else:
                    permission_check = False
                    messages.error(request,"Inactive device/account.")
                    Post_Device_Access(request, device, action="INACTIVE")
                    # DONE: Record Access in DeviceAccessLog
                    return HttpResponseRedirect(reverse('api:home'))

                # End of Insert
                # DONE: Call function to get permission

                if permission_check:
                    # We passed the checks so finish the login

                    django_login(request, user)
                    session_set = session_device(request, device.device)
                    # DONE: Record Access in DeviceAccessLog

                    dal_result = Post_Device_Access(request, device)
                    if settings.DEBUG:
                        print("Post to Device Access Log:", dal_result)

                    if settings.DEBUG:
                        print("User:", user)
                        print("Django_auth result:", auth_rslt)
                        print("Sessions:", request.session )

                    return HttpResponseRedirect(reverse('api:home'))
                else: # device.active = False
                    messages.error(request, "This is an inactive device account.")
                    return HttpResponseRedirect(reverse('api:home'))
            else: # Problem with account or password match
                messages.error(request, "Invalid device account or password.")
                return render_to_response('device/device_login.html',
                                          {'form': Device_AuthenticationForm()},
                                          RequestContext(request))
        else: # Problem with the form
            return render_to_response('device/device_login.html',
                                      {'form': form},
                                      RequestContext(request))
    else: # GET and not a POST - so setup form
        if settings.DEBUG:
            print("in Device_Login. Setting up Form")
        form = Device_AuthenticationForm()

    return render_to_response('device/device_login.html', {'form': form},
                              RequestContext(request))
