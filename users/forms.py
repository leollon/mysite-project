from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm as PasswdResetForm



class UserRegisterForm(forms.Form):
    username = forms.CharField(required=True, label=_('username'),
                               widget=forms.TextInput(
                                   attrs={'type': 'password'})
                               )
    email = forms.EmailField(required=True, label=_('email'))
    password = forms.CharField(required=True, label=_('password'),
                               widget=forms.TextInput(
                                   attrs={'type': 'password'})
                               )


class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(required=True, label=_('password'),
                               widget=forms.TextInput(
                                   attrs={'type': 'password'})
                               )
    submit = forms.CharField(label='',
                             widget=forms.TextInput(
                                 attrs={'type': 'submit'})
                             )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u'username and password is no '
                                        u'optional.')
        else:
            clean_data = super(UserLoginForm, self).clean()


class PasswordResetForm(PasswordChangeForm):
    pass


class PasswordResetRequestForm(PasswdResetForm):

    def __init__(self):
        pass
    pass

