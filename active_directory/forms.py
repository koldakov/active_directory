from django import forms
from .models import Settings
from django.utils.translation import gettext as _


class SettingsForm(forms.ModelForm):

    class Meta:
        model = Settings
        fields = ('domain', 'username', 'password', 'port', 'ssl')
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean(self):
        cleaned_data = super(SettingsForm, self).clean()
        username = cleaned_data.get('username')
        separators = ('@', '\\')

        if username.startswith(separators) or username.endswith(separators):
            raise forms.ValidationError(_(f'Username should not starts or ends with {" or ".join(separators)}.'))

        if not any(separator in username for separator in separators):
            raise forms.ValidationError(_(f'Username should contain {" or ".join(separators)}.'))
