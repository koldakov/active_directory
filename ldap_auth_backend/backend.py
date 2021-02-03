# Copyright (c) 2021, Ivan Koldakov.
# All rights not reserved.
#
# Use as you want, modify as you want but please include the author's name.

"""
LDAP authentication backend.
"""

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from active_directory.exceptions import LDAPAuthBackendException
from active_directory.utils.active_directory import get_users_ad
from active_directory.utils.active_directory import get_user_principal_name


class LDAPBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        username = self.clean_username(username)

        if not username:
            return None

        user_info = self.get_user_info(username, password)

        if not user_info:
            return None

        user = self.get_or_create_local_user(username)

        user = self.configure_user(user, user_info)

        return user

    def configure_user(self, user, user_info):
        """

        """

        # TODO mapping AD to User values and access rights according to active_directory.model.UserAccountControlValues
        #  and resolve types according to AD returning types.

        raw_attributes = user_info.get('raw_attributes')

        user.is_staff = True
        user.is_superuser = True
        user.email = raw_attributes.get('mail')[0].decode('utf-8')
        user.save()

        return user

    def clean_username(self, username):
        # Only userPrincipalName format. Pre-Windows 2000 has no chances
        return get_user_principal_name(username)

    def get_or_create_local_user(self, username):

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User.objects.create_user(username=username)

        return user

    def get_user(self, user_id):
        return User.objects.get(pk=user_id)

    @staticmethod
    def get_user_info(username, password):
        """

        """
        result = []

        for settings_ad_users_info in get_users_ad(
                login_username=username,
                login_password=password,
                users=[username.split('@')[0]]):
            for user_info in settings_ad_users_info:
                result.append(user_info)

        if len(result) == 1:
            return result[0]
        elif len(result) == 0:
            # No users found
            return None
        else:
            raise LDAPAuthBackendException('More than one users found for user %s' % username)
