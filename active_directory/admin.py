from django.contrib import admin
from .models import Settings
from .forms import SettingsForm


class SettingsAdmin(admin.ModelAdmin):
    form = SettingsForm
    list_per_page = 10
    list_display = ('domain', 'username', 'port', 'ssl')
    search_fields = ('domain', 'port', 'username')


admin.site.register(Settings, SettingsAdmin)
