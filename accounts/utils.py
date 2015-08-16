"""
developeraccount
FILE: utils
Created: 6/27/15 8:39 AM


"""

__author__ = 'Mark Scrimshire:@ekivemark'

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template import (RequestContext,
                             Context)
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

# Carrier Selection shows carriers with their email address
# All names must be unique
CARRIER_SELECTION = (('NONE', 'None'),
                     ('3 river wireless',
                      '3 river wireless(@sms.3rivers.net)'),
                     ('acs wireless',
                      'acs wireless(@paging.acswireless.com)'),
                     ('alltel', 'alltel(@message.alltel.com)'),
                     ('at&t', 'at&t(@txt.att.net)'),
                     ('bell canada', 'bell canada(@bellmobility.ca)'),
                     ('bell mobility txt',
                      'bell mobility(@txt.bellmobility.ca)'),
                     ('bell mobility (canada)',
                      'bell mobility (canada)(@txt.bell.ca)'),
                     ('blue sky frog', 'blue sky frog(@blueskyfrog.com)'),
                     ('bluegrass cellular',
                      'bluegrass cellular(@sms.bluecell.com)'),
                     ('boost mobile', 'boost mobile(@myboostmobile.com)'),
                     ('bpl mobile', 'bpl mobile(@bplmobile.com)'),
                     ('carolina west wireless',
                      'carolina west wireless(@cwwsms.com)'),
                     ('cellular one',
                      'cellular one(@mobile.celloneusa.com)'),
                     ('cellular south', 'cellular south(@csouth1.com)'),
                     ('centennial wireless',
                      'centennial wireless(@cwemail.com)'),
                     ('centurytel',
                      'centurytel(@messaging.centurytel.net)'),
                     ('cingular (now at&t)',
                      'cingular (now at&t)(@txt.att.net)'),
                     ('clearnet', 'clearnet(@msg.clearnet.com)'),
                     ('comcast', 'comcast(@comcastpcs.textmsg.com)'),
                     ('corr wireless communications',
                      'corr wireless communications(@corrwireless.net)'),
                     ('dobson', 'dobson(@mobile.dobson.net)'),
                     ('edge wireless',
                      'edge wireless(@sms.edgewireless.com)'),
                     ('fido', 'fido(@fido.ca)'),
                     ('golden telecom',
                      'golden telecom(@sms.goldentele.com)'),
                     ('helio', 'helio(@messaging.sprintpcs.com)'),
                     ('houston cellular',
                      'houston cellular(@text.houstoncellular.net)'),
                     ('idea cellular', 'idea cellular(@ideacellular.net)'),
                     ('illinois valley cellular',
                      'illinois valley cellular(@ivctext.com)'),
                     ('inland cellular telephone',
                      'inland cellular telephone(@inlandlink.com)'),
                     ('mci', 'mci(@pagemci.com)'),
                     ('metro pcs', 'metro pcs(@mymetropcs.com)'),
                     ('metrocall', 'metrocall(@page.metrocall.com)'),
                     ('metrocall 2-way', 'metrocall 2-way(@my2way.com)'),
                     ('microcell', 'microcell(@fido.ca)'),
                     ('midwest wireless',
                      'midwest wireless(@clearlydigital.com)'),
                     ('mobilcomm', 'mobilcomm(@mobilecomm.net)'),
                     ('mts', 'mts(@text.mtsmobility.com)'),
                     ('nextel', 'nextel(@messaging.nextel.com)'),
                     ('onlinebeep', 'onlinebeep(@onlinebeep.net)'),
                     ('pcs one', 'pcs one(@pcsone.net)'),
                     ('presidents choice',
                      'presidents choice(@txt.bell.ca)'),
                     ('public service cellular',
                      'public service cellular(@sms.pscel.com)'),
                     ('qwest', 'qwest(@qwestmp.com)'),
                     ('rogers at&t wireless',
                      'rogers at&t wireless(@pcs.rogers.com)'),
                     ('rogers canada', 'rogers canada(@pcs.rogers.com)'),
                     ('satellink', 'satellink(@satellink.net)'),
                     ('solo mobile', 'solo mobile(@txt.bell.ca)'),
                     ('southwestern bell',
                      'southwestern bell(@email.swbw.com)'),
                     ('sprint', 'sprint(@messaging.sprintpcs.com)'),
                     ('sumcom', 'sumcom(@tms.suncom.com)'),
                     ('surewest communications',
                      'surewest communications(@mobile.surewest.com)'),
                     ('t-mobile', 't-mobile(@tmomail.net)'),
                     ('telus', 'telus(@msg.telus.com)'),
                     ('tracfone', 'tracfone(@txt.att.net)'),
                     ('triton', 'triton(@tms.suncom.com)'),
                     ('unicel', 'unicel(@utext.com)'),
                     ('us cellular', 'us cellular(@email.uscc.net)'),
                     ('us west', 'us west(@uswestdatamail.com)'),
                     ('verizon', 'verizon(@vtext.com)'),
                     ('virgin mobile', 'virgin mobile(@vmobl.com)'),
                     ('virgin mobile canada',
                      'virgin mobile canada(@vmobile.ca)'),
                     ('west central wireless',
                      'west central wireless(@sms.wcc.net)'),
                     ('western wireless',
                      'western wireless(@cellularonewest.com)'),
                     )

# Use unique Carrier name to get email domain information
CARRIER_EMAIL_GATEWAY = (('None', 'NONE'),
                         ('3 river wireless', '@sms.3rivers.net'),
                         ('acs wireless', '@paging.acswireless.com'),
                         ('alltel', '@message.alltel.com'),
                         ('at&t', '@txt.att.net'),
                         ('bell canada', '@bellmobility.ca'),
                         ('bell canada', '@txt.bellmobility.ca'),
                         ('bell mobility txt', '@txt.bellmobility.ca'),
                         ('bell mobility (canada)', '@txt.bell.ca'),
                         ('blue sky frog', '@blueskyfrog.com'),
                         ('bluegrass cellular', '@sms.bluecell.com'),
                         ('boost mobile', '@myboostmobile.com'),
                         ('bpl mobile', '@bplmobile.com'),
                         ('carolina west wireless', '@cwwsms.com'),
                         ('cellular one', '@mobile.celloneusa.com'),
                         ('cellular south', '@csouth1.com'),
                         ('centennial wireless', '@cwemail.com'),
                         ('centurytel', '@messaging.centurytel.net'),
                         ('cingular (now at&t)', '@txt.att.net'),
                         ('clearnet', '@msg.clearnet.com'),
                         ('comcast', '@comcastpcs.textmsg.com'),
                         ('corr wireless communications',
                          '@corrwireless.net'),
                         ('dobson', '@mobile.dobson.net'),
                         ('edge wireless', '@sms.edgewireless.com'),
                         ('fido', '@fido.ca'),
                         ('golden telecom', '@sms.goldentele.com'),
                         ('helio', '@messaging.sprintpcs.com'),
                         ('houston cellular', '@text.houstoncellular.net'),
                         ('idea cellular', '@ideacellular.net'),
                         ('illinois valley cellular', '@ivctext.com'),
                         ('inland cellular telephone', '@inlandlink.com'),
                         ('mci', '@pagemci.com'),
                         ('metro pcs', '@mymetropcs.com'),
                         ('metrocall', '@page.metrocall.com'),
                         ('metrocall 2-way', '@my2way.com'),
                         ('microcell', '@fido.ca'),
                         ('midwest wireless', '@clearlydigital.com'),
                         ('mobilcomm', '@mobilecomm.net'),
                         ('mts', '@text.mtsmobility.com'),
                         ('nextel', '@messaging.nextel.com'),
                         ('onlinebeep', '@onlinebeep.net'),
                         ('pcs one', '@pcsone.net'),
                         ('presidents choice', '@txt.bell.ca'),
                         ('public service cellular', '@sms.pscel.com'),
                         ('qwest', '@qwestmp.com'),
                         ('rogers at&t wireless', '@pcs.rogers.com'),
                         ('rogers canada', '@pcs.rogers.com'),
                         ('satellink', '@satellink.net'),
                         ('solo mobile', '@txt.bell.ca'),
                         ('southwestern bell', '@email.swbw.com'),
                         ('sprint', '@messaging.sprintpcs.com'),
                         ('sumcom', '@tms.suncom.com'),
                         ('surewest communications',
                          '@mobile.surewest.com'),
                         ('t-mobile', '@tmomail.net'),
                         ('telus', '@msg.telus.com'),
                         ('tracfone', '@txt.att.net'),
                         ('triton', '@tms.suncom.com'),
                         ('unicel', '@utext.com'),
                         ('us cellular', '@email.uscc.net'),
                         ('us west', '@uswestdatamail.com'),
                         ('verizon', '@vtext.com'),
                         ('virgin mobile', '@vmobl.com'),
                         ('virgin mobile canada', '@vmobile.ca'),
                         ('west central wireless', '@sms.wcc.net'),
                         ('western wireless', '@cellularonewest.com'),
                         )


def strip_url(domain, www=None):
    """
    receive a URL Field and remove leading http:// or https://
    optionally remove www.
    :param url: eg. http://www.medyear.com
    :param www remove the prefix passed = "www."
    :return:
    """

    u = str(domain)
    u = u.lower()
    check_for_http = "http://"
    check_for_https = "https://"

    result = u.replace(check_for_http, "")
    result = result.replace(check_for_https, "")

    if www != None:
        result = result.replace(www.lower() + ".", "")

    return result


def email_mask(email=""):
    """
    mask and potentially shorten an email address
    Useful for communications
    :param email:
    :return:
    """

    if email=="":
        return None

    domain = "@"+email.split("@")[1]
    tld    = "."+domain.split(".")[1]

    if settings.DEBUG:
        print("Domain:",domain)

    result_email = email[:2]+"**" + domain[:2] + "**" + tld[:2] + "**"

    return result_email


def cell_email(phone, carrier):
    """
    Receive Phone number and carrier and return sms-email address
    :param phone:
    :param carrier:
    :return: email
    """
    if settings.DEBUG:
        print("Phone:", phone)
    # make sure it is in 10 digit phone number format
    # no + or . or - or ( or )
    if phone == None:
        return None

    # We have a phone number so let's get the email address
    phone_digits = str(phone)
    phone_digits = phone_digits.replace("+1", "")

    # Now we need to check the carrier

    if (carrier == "" or carrier == "NONE" or carrier == None):
        return None

    # We have a phone and a carrier
    if settings.DEBUG:
        print(carrier)
    # lookup email
    carrier_email = dict(CARRIER_EMAIL_GATEWAY)
    carrier_address = carrier_email[carrier]

    email = "%s%s" % (phone_digits, carrier_address)

    return email


def send_sms_pin(email, pin):
    """
    Send a text with an SMS code

    :param email:
    :return:
    """

    subject = ""
    msg = "%s pin:%s" % (settings.APPLICATION_TITLE, pin)
    from_email = settings.EMAIL_HOST_USER
    send_to = []
    send_to.append(email)
    if settings.DEBUG:
        print("Sending %s to %s" % (msg, send_to))

    try:
        result = send_mail(subject, msg, from_email, send_to,
                           fail_silently=False)
        if settings.DEBUG:
            print("Result of send:", result)
    except:
        result = "FAIL"

    if settings.DEBUG:
        print("Send Result:", result)

    return result


def build_message_text(request,context={},
                       template="",
                       extn="txt",
                       ):
    """
    Compose a message to include in an email message
    :param request:
    :param template:
    :param extn: txt, html or sms
            (this becomes the file extension for the template)
            sms is a brief template suitable for SMS Text Messages
    :param email:
    :return:
    """
    # Template files use the Django Template System.

    ctxt = {}
    if context is not None:
        # print("BMT:Context is:", context)
        ctxt = RequestContext(request, context)
        # print("BMT:ctxt with context:", ctxt)

    if request is not None:
        # print("BMT:Request is:", request)
        ctxt = RequestContext(request, ctxt)

    # if settings.DEBUG:
    #     print("BMT:Context ctxt is:", ctxt)

    if template=="":
        template="accounts/messages/account_activity_email"

    source_plate = template + "." + extn

    message = render_to_string(source_plate, ctxt)
    if settings.DEBUG:
        print("Message:",message)

    return message


def send_activity_message(request,
                          user,
                          subject="",
                          template="",
                          msg="",
                          context={}
                          ):
    """
    Send an email
    """
    # Template files use the Django Template System.

    phone_email_to = cell_email(user.mobile, user.carrier)
    email          = user.email
    from_email     = settings.EMAIL_HOST_USER
    send_to        = []
    message_txt    = ""
    message_html   = ""

    ctx_dict = {}
    if request is not None:
        # if settings.DEBUG:
        #     print("Request is this:",request)
        ctx_dict = RequestContext(request, ctx_dict)

    # User_Model = get_user_model()
    # usermodel = User_Model.objects.get(email=email)
    ctx_dict.update({
        'email': email,
        'user' : user,
        'msg'  : msg,
        'site' : Site.objects.get_current(),
        })

    if context is not None:
        ctx_dict.update(context)

    if settings.DEBUG:
        print("SAM-ctx_dict:", ctx_dict)

    from_email = getattr(settings, 'REGISTRATION_DEFAULT_FROM_EMAIL',
                         settings.DEFAULT_FROM_EMAIL)

    if user.notify_activity.upper() == "E":
        if subject=="":
            subject = settings.APPLICATION_TITLE + " Account Activity for " + email


        # Otherwise we take the subject line passed in to the function
        # Remove any newlines from subject
        subject = ''.join(subject.splitlines())

        # Now we will build the message
        send_to.append(email)
        message_txt = build_message_text(request,
                                         context=ctx_dict,
                                         template=template,
                                         extn="txt")
        if settings.EMAIL_HTML:
            # If True: Generate and attach the HTML version
            message_html = build_message_text(request,
                                              context=ctx_dict,
                                              template=template,
                                              extn="html")
    if user.notify_activity.upper() == "T":
        # Text messages do not have subject lines so we need to reset
        subject = ""
        send_to.append(phone_email_to)

        message_txt = build_message_text(request,
                                         context=ctx_dict,
                                         template=template,
                                         extn="sms")

    if settings.DEBUG:
        print("Sending:", send_to)
        print("Subject:", subject)
        print("Message:", message_txt)

    email = EmailMultiAlternatives(subject,
                                   message_txt,
                                   from_email,
                                   send_to,
                                   )
    if not message_html == "":
        # If html was created we should attach it before message is sent
        email.attach_alternative(message_html, "text/html")

    try:
        result = email.send(fail_silently=False)
        if settings.DEBUG:
            print("Result of Send:", result)
    except:
        result = "FAIL"
        if settings.DEBUG:
            print("Send Failed with:", result)

    return result

