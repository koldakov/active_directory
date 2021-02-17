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
from active_directory.exceptions import LDAPException
import ldap3


def fix_types(entry):
    # TODO fix encodings, auto_encode (Connection) in ldap3-2.9 does not work well? Everything in bytes,
    #  should fix manually?
    return entry


def get_user_principal_name(username):
    """
    :username: username
    :return: user normal name (userPrincipalName) or None
    """

    if username is None:
        return None

    username = str(username)

    if '@' in username:
        return username
    elif '\\' in username:
        # For mammoths
        # domain\username is the same as username@domain
        return '@'.join(reversed(username.split('\\')))
    else:
        return None


def get_search_base(username):
    """
    :username: username
    :return: search base or distinguished name (dn)
    """
    return ''.join(['dc=%s,' % u for u in username.split('@')[1].split('.')]).strip(',')


def get_settings_ad(settings_ad_type=None):
    """
    :settings_ad_type: this parameter allows to get AD settings from different places: model, settings.py, etc
    :return: iterator (it can be list) of all settings
    """
    if not settings_ad_type:
        return SettingsActiveDirectory.objects.all().iterator()


def get_connections_ad(login_username=None, login_password=None):
    """
    :login_username: username to establish ldap connection. Use settings login if None
    :login_password: password to establish ldap connection. Use settings password if None
    :yield: search base (distinguished name) and ldap connection OR None, None
    """

    for settings_ad in get_settings_ad():
        # Search in all AD settings. It can be different domain controllers, users and so on
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


def get_users_info_ad(login_username=None, login_password=None, users=None, attributes='*'):
    """
    :login_username: username to establish ldap connection. Use settings login if None
    :login_password: password to establish ldap connection. Use settings password if None
    :users: must be list of users (['user1', .., 'userN']) to search users user1, .., userN or None to search all users
    :attributes: ldap parameter, can be * to search all attributes, or you can specify individual: ['mail']
    :return: results from different settings
    """

    if not users:
        search_filter = '(objectClass=person)'
    else:
        if not isinstance(users, list):
            raise LDAPException('Users must be list of users or None')

        search_filter = '(&(objectClass=person)(|%s))' % ''.join(
            ['(sAMAccountName=%s)' % user.strip() for user in users])

    results = []

    for search_base, conn in get_connections_ad(login_username=login_username, login_password=login_password):
        # Search in all settings
        if conn is None:
            # TODO notify user (system administrator ?) that AD settings does not work
            # Continue to the next settings
            continue

        for entry in conn.extend.standard.paged_search(
            search_base=search_base,
            search_filter=search_filter,
            search_scope=ldap3.SUBTREE,
            attributes=attributes,
            paged_size=500,
            generator=True
        ):
            # Remove searchResRef results
            if entry.get('type') != 'searchResRef':
                results.append(fix_types(entry))

        conn.unbind()

    # It's normal not to yield but to return here
    # TODO think: or yield each result?
    return results
