from django import forms
from .models import Settings


class SettingsForm(forms.ModelForm):

    class Meta:
        model = Settings
        fields = ('domain', 'username', 'password', 'port', 'ssl')
        widgets = {
            'password': forms.PasswordInput(),
        }
