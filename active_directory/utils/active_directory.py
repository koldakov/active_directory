# Copyright (c) 2021, Ivan Koldakov.
# All rights not reserved.
#
# Use as you want, modify as you want but please include the author's name.

"""
This util is used for working with active directory.
"""

from active_directory.models import Settings
from ldap3.core.exceptions import LDAPException


def get_users_info_ad(login_username=None, login_password=None, users=None, domains=None, attributes='*'):
    """
    :login_username: username to establish ldap connection. Use settings login if None
    :login_password: password to establish ldap connection. Use settings password if None
    :users: must be list/tuple of users to search users or None to search all users
    :attributes: ldap parameter, can be * to search all attributes, or you can specify individual: ['mail']
    :return: results from different settings
    """

    results = []

    if not domains:
        settings = Settings.objects.all()
    else:
        settings = Settings.objects.filter(domain__in=domains)

    if not settings:
        raise LDAPException('No active AD connections found')

    for setting in settings:
        try:
            result = setting.get_users_info_ad(
                login_username=login_username, login_password=login_password, users=users, attributes=attributes)
            results.extend(result)
        except LDAPException as e:
            print(f'Error \'{e}\' in AD settings {setting}')
            continue

    return results
