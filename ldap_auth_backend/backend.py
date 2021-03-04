# Copyright (c) 2021, Ivan Koldakov.
# All rights not reserved.
#
# Use as you want, modify as you want but please include the author's name.

"""
LDAP authentication backend.
"""

from active_directory.exceptions import LDAPAuthBackendException
from active_directory.utils.active_directory import get_users_info_ad
from active_directory.utils.active_directory import get_user_principal_name
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class LDAPBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        username = self.clean_username(username)

        if not username:
            # Not AD username format. domain\username or username@domain only
            return None

        user_info = self.get_user_info(username, password)

        if not user_info:
            return None

        user = self.configure_user(self.get_or_create_local_user(username), user_info)

        return user

    def configure_user(self, user, user_info):
        """ Modify user based on AD information.
        :user: django User object
        :user_info: user information from AD
        :return: modified django User
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
        :username: username of AD user
        :password: password of AD user
        :return: None if user not found in AD, dict with user AD info if user found
        :raise: LDAPAuthBackendException if found more than one user in AD
        """
        results = get_users_info_ad(
                login_username=username,
                login_password=password,
                users=[username.split('@')[0]])

        if len(results) == 1:
            return results[0]
        elif len(results) == 0:
            # No users found
            return None
        else:
            # This means that AD is configured wrong
            # TODO think should we raise exception or notify user (system administrator ?) or just return None
            raise LDAPAuthBackendException(f'More than one user found for user {username}')
