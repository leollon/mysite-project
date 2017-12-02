from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import PasswordResetForm as PasswdResetForm

from users.models import User


class UserRegisterForm(UserCreationForm):
    """
    This form class is for visitor to Create account
    """

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    username = forms.CharField(required=True,
                               label=_('Username'),
                               label_suffix='',
                               widget=forms.TextInput(
                                   attrs={"class": "form-control",
                                          "autofocus": True,
                                          "placeholder": _("Username")}
                                   )
                               )
    email = forms.EmailField(required=True, label=_('Email'),
                             label_suffix='',
                             widget=forms.EmailInput(
                                 attrs={"class": "form-control",
                                        "autofocus": False,
                                        "placeholder": _("Email")}
                                 )
                             )
    password1 = forms.CharField(required=True,
                                label=_('Password'),
                                label_suffix='',
                                widget=forms.PasswordInput(
                                   attrs={"class": "form-control",
                                          "type": "password",
                                          "placeholder": _("Password")}
                                   )
                                )
    password2 = forms.CharField(required=True,
                                label=_('Confirm Password'),
                                label_suffix='',
                                widget=forms.PasswordInput(
                                    attrs={"class": "form-control",
                                           "type": "password",
                                           "placeholder": _("Confirm \
                                                            Password")})
                                )
    submit = forms.CharField(label='',
                             widget=forms.TextInput(
                                 attrs={"class": "btn btn-default",
                                        "type": "submit",
                                        "value": _("SignUp")})
                             )

    def clean_email(self):
        """
        To check the user's input email whether is available.
        :return: user's email or raise error if the email is unavailable.
        """
        try:
            User.objects.get(email=self.cleaned_data.get('email'))
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(_('This email has been registered.'))
        return self.cleaned_data.get('email')


class UserLoginForm(forms.Form):
    """
    Login form class to create an login form for user to login this site
    """
    email = forms.EmailField(label_suffix='',
                             widget=forms.EmailInput(
                                            attrs={"class": "form-control",
                                                   "autofocus": True,
                                                   "placeholder": _("Email")}
                                            )
                             )
    password = forms.CharField(required=True, label=_('Password'),
                               widget=forms.TextInput(
                                   attrs={"class": "form-control",
                                          "type": "password",
                                          "placeholder": _("Password")}
                                   )
                               )
    submit = forms.CharField(label='',
                             widget=forms.TextInput(
                                 attrs={"class": "btn btn-default",
                                        "type": "submit",
                                        "value": _("Login")}
                                 )
                             )

    def clean(self):
        """
        Check if a user has input his/her email
        :return: cleaned_data or raise error if user did not input email address
        """
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

