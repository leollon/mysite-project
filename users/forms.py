from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm as PasswdResetForm

from users.models import User


class UserRegisterForm(UserCreationForm):

    username = forms.CharField(required=True,
                               label=_('Username'),
                               label_suffix='',
                               widget=forms.TextInput(
                                   attrs={"class": "form-control",
                                          "autofocus": True,
                                          "placeholder": "Username"})
                               )
    email = forms.EmailField(required=True, label=_('Email'),
                             label_suffix='',
                             widget=forms.EmailInput(
                                 attrs={"class": "form-control",
                                        "autofocus": False,
                                        "placeholder": "Email"})
                             )
    password1 = forms.CharField(required=True,
                                label=_('Password'),
                                label_suffix='',
                                widget=forms.PasswordInput(
                                   attrs={"class": "form-control",
                                          "type": "password",
                                          "placeholder": "Password"})
                                )
    password2 = forms.CharField(required=True,
                                label=_('Confirm Password'),
                                label_suffix='',
                                widget=forms.PasswordInput(
                                    attrs={"class": "form-control",
                                           "type": "password",
                                           "placeholder": "Confirm Password"})
                                )
    submit = forms.CharField(label='',
                             widget=forms.TextInput(
                                 attrs={"class": "btn btn-default",
                                        "type": "submit",
                                        "value": _("SignUp")})
                             )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(_('This email has been registered.'))
        return self.cleaned_data.get('email')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(forms.Form):
    email = forms.EmailField(label_suffix='',
                             widget=forms.EmailInput(
                                            attrs={"class": "form-control",
                                                   "autofocus": True,
                                                   "placeholder": "Email"})
                             )
    password = forms.CharField(required=True, label=_('Password'),
                               widget=forms.TextInput(
                                   attrs={"class": "form-control",
                                          "type": "password",
                                          "placeholder": "Password"})
                               )
    submit = forms.CharField(label='',
                             widget=forms.TextInput(
                                 attrs={"class": "btn btn-default",
                                        "type": "submit",
                                        "value": _("Login")})
                             )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError('email and password is not \
                                        optional.')
        else:
            return super(UserLoginForm, self).clean()


class PasswordResetForm(PasswordChangeForm):
    pass


class PasswordResetRequestForm(PasswdResetForm):

    def __init__(self):
        pass

