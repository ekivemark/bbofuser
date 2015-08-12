"""
bbofuser:account
FILE: ldap
Created: 8/11/15 3:17 PM

LDAP Utilities for Account

"""
__author__ = 'Mark Scrimshire:@ekivemark'

# import ldap

from django.conf import settings
from django.contrib import messages


def validate_ldap_user(request, email):
    # Do the ldapSearch for user
    result = {}
    if email == "":
        return result

    # Patch
    return email.lower()
    # Patch

    l = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
    try:
        l.simple_bind_s("", "")
        # We only want LDAP to return information for the specific email user
        user_scope = "cn=" + email + "," + settings.AUTH_LDAP_SCOPE

        if settings.DEBUG:
            print("user_scope:", user_scope)
        try:
            ldap_result = l.search_s(user_scope,
                                     ldap.SCOPE_SUBTREE, "objectclass=*")
        except:
            ldap_result = []
        if settings.DEBUG:
            print("ldap returned:", ldap_result)

        # ldap returned:
        # ('cn=mark@ekivemark.com,ou=people,dc=bbonfhir,dc=com',
        # {'sn': [b'Scrimshire'], 'givenName': [b'Mark'],
        # 'cn': [b'mark@ekivemark.com'],
        # 'mail': [b'mark@ekivemark.com'],
        # 'objectClass': [b'inetOrgPerson'],
        # 'displayName': [b'Mark Scrimshire']}
        # )

        if ldap_result == []:
            result = ""
        else:
            result_subset = ldap_result[0][1]
            result_mail = result_subset['mail']
            result = result_mail[0].decode("utf-8")
            if settings.DEBUG:
                print("email:", result)

    except ldap.SERVER_DOWN:
        if settings.DEBUG:
            print("LDAP Server", settings.AUTH_LDAP_SERVER_URI, "is Down")
        messages.error(request,
                       "We are unable to unable to confirm your email address at this time. Please try again later.")
        result = "ERROR"
    except ldap.LDAPError:
        if settings.DEBUG:
            print("LDAP Server error:", settings.AUTH_LDAP_SERVER_URI)
        messages.error(request,
                       "We had a problem reaching MyMedicare.gov. Please try again later.")
        result = "ERROR"

    return result

