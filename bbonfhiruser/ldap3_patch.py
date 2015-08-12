"""
bbofuser
FILE: ldap3_patch
Created: 8/11/15 10:44 PM


"""
__author__ = 'Mark Scrimshire:@ekivemark'



# django-auth-ldap
AUTH_LDAP_SERVER_URI = "ldap://dev.bbonfhir.com:389"
LDAP_AUTH_URL = AUTH_LDAP_SERVER_URI
LDAP_AUTH_USE_TLS = False

AUTH_LDAP_BIND_DN = "cn=django-agent,dc=bbonfhir,dc=com"

from ldap3 import Server, Connection, ALL



############## LDAP SEARCH Test
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=people,dc=bbonfhir,dc=com",
                                   ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
##############
# Pull from local.ini and remove surrounding double quotes
AUTH_LDAP_SCOPE = parser.get('global', 'auth_ldap_scope').strip()
AUTH_LDAP_SCOPE = AUTH_LDAP_SCOPE.replace('"', '')
if AUTH_LDAP_SCOPE == "":
    AUTH_LDAP_SCOPE = "ou=people,dc=bbonfhir,dc=com"
LDAP_AUTH_SEARCH_BASE = AUTH_LDAP_SCOPE
LDAP_AUTH_OBJECT_CLASS = "inetOrgPerson"
LDAP_AUTH_CONNECTION_USERNAME = None
LDAP_AUTH_CONNECTION_PASSWORD = None
LDAP_AUTH_USER_FIELDS = {
    "username": "uid",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}
LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)





#LDAP_AUTH_CLEAN_USER_DATA = django_python3_ldap.utils.clean_user_data

# ##############
# from ldap3 import Server, Connection, SUBTREE
# total_entries = 0
server = Server(AUTH_LDAP_SERVER_URI, get_info=ALL)
c = Connection(server,)

# c.search(search_base = 'o=test',
#          search_filter = '(objectClass=inetOrgPerson)',
#          search_scope = SUBTREE,
#          attributes = ['cn', 'givenName'],
#          paged_size = 5)
# total_entries += len(c.response)
# for entry in c.response:
#     print(entry['dn'], entry['attributes'])
#
# cookie = c.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
# while cookie:
#     c.search(search_base = 'o=test',
#              search_filter = '(object_class=inetOrgPerson)',
#              search_scope = SUBTREE,
#              attributes = ['cn', 'givenName'],
#              paged_size = 5,
#              paged_cookie = cookie)
#     total_entries += len(c.response)
#     cookie = c.result['controls']['1.2.840.113556.1.4.319']['value']['cookie']
#     for entry in c.response:
#         print(entry['dn'], entry['attributes'])
# print('Total entries retrieved:', total_entries)
#
#
# ##############

FHIR_SERVER = parser.get('global', 'fhir_server')
if FHIR_SERVER == '':
    FHIR_SERVER = 'http://fhir.bbonfhir.com:8080/fhir-p'
    # FHIR_SERVER = 'http://localhost:8080/fhir-p'

if DEBUG_SETTINGS:
    print("FHIR_SERVER:", FHIR_SERVER)
    print("AUTH_LDAP_SCOPE:", AUTH_LDAP_SCOPE)
    l = ldap.initialize(AUTH_LDAP_SERVER_URI)
    try:
        l.simple_bind_s("", "")
        ldap_result = l.search_s(AUTH_LDAP_SCOPE,
                                 ldap.SCOPE_SUBTREE,
                                 "objectclass=*")
        print("=========================================")
        print("LDAP Access Test:")
        for key, value in ldap_result:
            print("key:", key, ": ", value)
        print("=========================================")
#
    except ldap.SERVER_DOWN:
        print("ERROR! LDAP Server:", AUTH_LDAP_SERVER_URI,
              "is not accessible")
#
    except ldap.LDAPError:
        print("LDAP Error:")


