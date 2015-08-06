"""
developeraccount
FILE: utils
Created: 6/27/15 8:39 AM


"""
__author__ = 'Mark Scrimshire:@ekivemark'

from django.core.mail import send_mail
from django.conf import settings

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


def cell_email(phone, carrier):
    """
    Receive Phone number and carrier and return sms-email address
    :param phone:
    :param carrier:
    :return: email
    """
    if settings.DEBUG:
        print(phone)
    # make sure it is in 10 digit phone number format
    # no + or . or - or ( or )
    phone_digits = str(phone)
    phone_digits = phone_digits.replace("+1", "")

    if (carrier == "" or carrier == None):
        return None

    if settings.DEBUG:
        print(carrier)
    # lookup email
    carrier_email = dict(CARRIER_EMAIL_GATEWAY)
    carrier_address = carrier_email[carrier]

    email = "%s%s" % (phone_digits, carrier_address)

    return email


def send_sms_pin(phone, email, pin):
    """
    Send a text with an SMS code
    :param phone:
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

