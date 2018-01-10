from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
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
                                           "placeholder": _("Confirm Password")}
                                    )
                                )
    submit = forms.CharField(label='',
                             widget=forms.TextInput(
                                 attrs={"class": "btn btn-default",
                                        "type": "submit",
                                        "value": _("SignUp")}
                                 )
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
            raise forms.ValidationError('The email and password is not \
                                        optional.')
        else:
            return super(UserLoginForm, self).clean()


class PasswordResetRequestForm(PasswdResetForm):
    """
    This form class is for inputting email address when a user request to
    change password.
    """
    email = forms.EmailField(label_suffix='',
                             max_length=254,
                             widget=forms.EmailInput(
                                 attrs={"class": "form-control",
                                        "autofocus": True,
                                        "placeholder": _("Your email address")}
                                 )
                             )
    submit = forms.CharField(label='',
                             widget=forms.TextInput(
                                 attrs={"class": "btn btn-default",
                                        "type": "submit",
                                        "value": _("Send")}
                                 )
                             )

    def clean_email(self):
        """
        Check user's email inputted whether exists in database
        :return: cleaned_data
        """
        try:
            User.objects.get(email=self.cleaned_data.get('email'))
        except User.DoesNotExist:
            raise forms.ValidationError(_('Wrong email address.'))
        else:
            return super(PasswordResetRequestForm, self).clean()


class PasswordResetForm(forms.Form):
    """
    This form class is for changing user's password by entering its old password
    """
    def __init__(self, user, data=None, *args, **kwargs):
        self.user = user
        super(PasswordResetForm, self).__init__(data, *args, **kwargs)

    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_incorrect': _("The password is incorrect"),
    }
    old_password = forms.CharField(label=_("Old Password"),
                                   label_suffix="",
                                   strip=False,
                                   widget=forms.PasswordInput(
                                       attrs={"class": "form-control",
                                              "type": "password",
                                              "placeholder": _("Old password")}
                                       )
                                   )
    new_password1 = forms.CharField(label=_("New Password"),
                                    label_suffix="",
                                    strip=False,
                                    help_text=password_validation.password_validators_help_text_html(),
                                    widget=forms.PasswordInput(
                                        attrs={"class": "form-control",
                                               "type": "password",
                                               "placeholder": _("New password")}
                                        )
                                    )
    new_password2 = forms.CharField(label=_("Confirm Password"),
                                    label_suffix="",
                                    strip=False,
                                    widget=forms.PasswordInput(
                                        attrs={"class": "form-control",
                                               "type": "password",
                                               "placeholder": _("Confirm new "
                                                                "password")}
                                        )
                                    )
    submit = forms.CharField(label='',
                             widget=forms.TextInput(
                                 attrs={"class": "btn btn-default",
                                        "type": "submit",
                                        "value": _("Save")}
                                 )
                             )

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect')
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data['new_password1']
        password2 = self.cleaned_data['new_password2']
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
                )
        password_validation.validate_password(password2, self.user)
        return password2
