# Copyright (c) 2021, Ivan Koldakov.
# All rights not reserved.
#
# Use as you want, modify as you want but please include the author's name.

"""
This util is used for working with active directory.
Module moved to external file to isolate working with AD.
Using this module you can expand everything you want. Management commands for example.

By default active directory settings are getting from SettingsActiveDirectory, you can easily change it by
modifying get_settings_ad function.
Example:

def get_settings_ad(settings_ad_type=None):
    if not settings_ad_type:
        return settings.get('SETTINGS_AD')
    elif settings_ad_type == 'model_object':
        return SettingsActiveDirectory.objects.all().iterator()

settings is settings.py file,
SETTINGS_AD format is (different domain settings are allowed!):
[
    {
        username_ad: 'username_ad',
        password_ad: 'password_ad',
        domain_ad: 'domain_ad',
        ssl_ad: False,
        port_ad: 389
    },
    {
        username_ad: 'username_ad_2',
        password_ad: 'password_ad_2',
        domain_ad: 'domain_ad_2',
        ssl_ad: True,
        port_ad: 636
    },
]

Moreover you can abstract from django and use this file in your own project to work with AD
just remove SettingsActiveDirectory.
"""

from active_directory.models import SettingsActiveDirectory
from active_directory.exceptions import LDAPAuthBackendException
import ldap3


def get_user_principal_name(username):
    """
    :username: username
    :returns: user normal name (userPrincipalName)
    """
    if '@' in username:
        return username
    # For mammoths
    elif '\\' in username:
        return '@'.join(reversed(username.split('\\')))
    else:
        return None


def get_search_base(username):
    """
    :username: username
    :returns: search base or distinguished name (dn)
    """
    return ''.join(['dc=%s,' % u for u in username.split('@')[1].split('.')]).strip(',')


def get_settings_ad(settings_ad_type=None):
    """
    :settings_ad_type: this parameter allows to get AD settings from different places: model, settings.py, etc
    :returns: iterator (it can be list) of all settings
    """
    if not settings_ad_type:
        # TODO think about searching in all settings. May be need just one? It will simplify everything!
        return SettingsActiveDirectory.objects.all().iterator()


def get_connections_ad(login_username=None, login_password=None):
    """
    :login_username: username to establish ldap connection. Use settings login if None
    :login_password: password to establish ldap connection. Use settings password if None
    :yields: search base (distinguished name) and ldap connection OR None, None
    """

    for settings_ad in get_settings_ad():

        if not login_username:
            login_username = settings_ad.username_ad
            login_password = settings_ad.password_ad

        server = ldap3.Server(settings_ad.domain_ad, port=settings_ad.port_ad, use_ssl=settings_ad.ssl_ad,
                              get_info=ldap3.ALL)
        username_ad = get_user_principal_name(login_username)

        search_base = get_search_base(username_ad)

        try:
            yield search_base, ldap3.Connection(server, username_ad, login_password, auto_bind=True)
        except ldap3.core.exceptions.LDAPSocketOpenError:
            yield None, None
        except ldap3.core.exceptions.LDAPBindError:
            yield None, None


def get_users_ad(login_username=None, login_password=None, users=None, attributes='*'):
    """
    :login_username: username to establish ldap connection. Use settings login if None
    :login_password: password to establish ldap connection. Use settings password if None
    :users: must be list of users (['user1', 'user2']) to search users user1 and user2 or None to search all users
    :attributes: ldap parameter, can be * to search all attributes, or you can specify individual: ['mail']
    :yields: results from different settings
    """

    if not users:
        search_filter = '(objectClass=person)'
    else:
        if not isinstance(users, list):
            raise LDAPAuthBackendException('Users must be list of users or None')

        search_filter = '(&(objectClass=person)(|%s))' % ''.join(['(sAMAccountName=%s)' % user for user in users])

    for search_base, conn in get_connections_ad(login_username=login_username, login_password=login_password):
        if conn is None:
            # TODO notify user (system administrator ?) that AD settings does not work
            # Continue to the next settings
            continue

        entry_generator = conn.extend.standard.paged_search(
            search_base=search_base,
            search_filter=search_filter,
            search_scope=ldap3.SUBTREE,
            attributes=attributes,
            paged_size=500,
            generator=True
        )

        results = []

        for entry in entry_generator:
            # Remove searchResRef results
            if entry.get('type') != 'searchResRef':
                results.append(entry)

        conn.unbind()

        yield results
