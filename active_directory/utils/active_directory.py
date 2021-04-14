# Copyright (c) 2021, Ivan Koldakov.
# All rights not reserved.
#
# Use as you want, modify as you want but please include the author's name.

"""
This util is used for working with active directory.
"""

from active_directory.models import Settings
from ldap3.core.exceptions import LDAPException


def get_users_info_ad(login_username=None, login_password=None, users=None, attributes='*'):
    """
    :login_username: username to establish ldap connection. Use settings login if None
    :login_password: password to establish ldap connection. Use settings password if None
    :users: must be list/tuple of users to search users or None to search all users
    :attributes: ldap parameter, can be * to search all attributes, or you can specify individual: ['mail']
    :return: results from different settings
    """

    results = []

    for ad_setting in Settings.objects.all():
        try:
            results.extend(
                ad_setting.get_users_info_ad(
                    login_username=login_username, login_password=login_password, users=users, attributes=attributes)
            )
        except LDAPException:
            continue

    return results
