from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ActiveDirectoryConfig(AppConfig):
    name = 'active_directory'
    verbose_name = _("Active directory")
