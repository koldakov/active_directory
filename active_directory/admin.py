from django.contrib import admin
from .models import Settings
from .forms import SettingsForm


class SettingsAdmin(admin.ModelAdmin):
    form = SettingsForm


admin.site.register(Settings, SettingsAdmin)
