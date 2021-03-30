from django import forms
from .models import SettingsActiveDirectory


class SettingsActiveDirectoryForm(forms.ModelForm):

    class Meta:
        model = SettingsActiveDirectory
        fields = ('domain', 'username', 'password', 'port', 'ssl')
        widgets = {
            'password': forms.PasswordInput(),
        }
