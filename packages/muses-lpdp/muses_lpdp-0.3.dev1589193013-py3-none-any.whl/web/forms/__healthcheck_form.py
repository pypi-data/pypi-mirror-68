from django import forms
from django.utils.translation import gettext_lazy as _

from web.forms import MultiForm
from web.forms.widgets import EmailInput


class CheckEmailForm(MultiForm):
    email = forms.EmailField(widget=EmailInput, label=_('Email'), required=True)

    def send_email(self):
        pass
