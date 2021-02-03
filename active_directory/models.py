from django.db import models
from django.utils.translation import gettext_lazy as _


class SettingsActiveDirectory(models.Model):
    username_ad = models.CharField(_('AD Username'), max_length=150, null=False, blank=False)
    password_ad = models.CharField(_('Password of AD user'), max_length=128, null=False, blank=False)
    domain_ad = models.CharField(_('Domain controller'), max_length=256, null=False, blank=False)
    ssl_ad = models.BooleanField(_('SSL'), default=False, null=False, blank=False)
    port_ad = models.PositiveIntegerField(_('Active directory port'), default=389, blank=False)

    def __str__(self):
        return str(self.domain_ad)


# https://docs.microsoft.com/ru-ru/troubleshoot/windows-server/identity/useraccountcontrol-manipulate-account-properties
class UserAccountControlValues(object):
    SCRIPT = 1
    ACCOUNTDISABLE = 2
    HOMEDIR_REQUIRED = 8
    LOCKOUT = 16
    PASSWD_NOTREQD = 32
    PASSWD_CANT_CHANGE = 64
    ENCRYPTED_TEXT_PWD_ALLOWED = 128
    TEMP_DUPLICATE_ACCOUNT = 256
    NORMAL_ACCOUNT = 512
    INTERDOMAIN_TRUST_ACCOUNT = 2048
    WORKSTATION_TRUST_ACCOUNT = 4096
    SERVER_TRUST_ACCOUNT = 8192
    DONT_EXPIRE_PASSWORD = 65536
    MNS_LOGON_ACCOUNT = 131072
    SMARTCARD_REQUIRED = 262144
    TRUSTED_FOR_DELEGATION = 524288
    NOT_DELEGATED = 1048576
    USE_DES_KEY_ONLY = 2097152
    DONT_REQ_PREAUTH = 4194304
    PASSWORD_EXPIRED = 8388608
    TRUSTED_TO_AUTH_FOR_DELEGATION = 16777216
    PARTIAL_SECRETS_ACCOUNT = 67108864
