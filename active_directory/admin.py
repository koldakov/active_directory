from django.contrib.auth import get_permission_codename
from django.contrib import admin
from .forms import SettingsForm
from .forms import ADUserForm
from .models import Settings
from .models import ADUser
from .utils.admin_actions import change_fields
from .utils.admin_actions import get_csv


class SettingsAdmin(admin.ModelAdmin):
    form = SettingsForm
    list_per_page = 10
    list_display = ('domain', 'username', 'port', 'ssl')
    search_fields = ('domain', 'port', 'username')
    actions = [change_fields, get_csv]

    def has_change_fields_permission(self, request):
        codename = get_permission_codename('change', self.opts)
        app_label = self.opts.app_label

        return request.user.has_perm(f'{app_label}.{codename}')

    def has_get_csv_permission(self, request):
        codename = get_permission_codename('view', self.opts)
        app_label = self.opts.app_label

        return request.user.has_perm(f'{app_label}.{codename}')


class ADUserAdmin(admin.ModelAdmin):
    form = ADUserForm
    list_per_page = 10
    list_display = ('username', 'mail', 'organizational_unit')
    search_fields = ('username', 'mail', 'organizational_unit')
    actions = [change_fields, get_csv]

    def has_add_permission(self, request):
        return False

    def has_change_fields_permission(self, request):
        codename = get_permission_codename('change', self.opts)
        app_label = self.opts.app_label

        return request.user.has_perm(f'{app_label}.{codename}')

    def has_get_csv_permission(self, request):
        codename = get_permission_codename('view', self.opts)
        app_label = self.opts.app_label

        return request.user.has_perm(f'{app_label}.{codename}')


admin.site.register(Settings, SettingsAdmin)
admin.site.register(ADUser, ADUserAdmin)
