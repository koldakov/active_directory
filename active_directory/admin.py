from django.contrib import admin
from .models import SettingsActiveDirectory
from .forms import SettingsActiveDirectoryForm


class SettingsActiveDirectoryAdmin(admin.ModelAdmin):
    form = SettingsActiveDirectoryForm


admin.site.register(SettingsActiveDirectory, SettingsActiveDirectoryAdmin)
