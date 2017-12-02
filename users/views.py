from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _

from users.models import User
from users.forms import UserLoginForm, UserRegisterForm, \
                        PasswordResetForm, PasswordResetRequestForm

from users.utils import notify_user


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create(username=form.cleaned_data['username'],
                                       email=form.cleaned_data['email'])
            user.set_password(form.cleaned_data['password1'])
            notify_user(form=form, token=user.generate_valid_token())
            user.save()
            return HttpResponseRedirect(reverse('users:login'))
        else:
            return render(request, 'users/register.html', {'form': form})
    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})


@login_required
def validate_view(request, token):
    """
    :param request: HttpRequest object
    :param token: user's activating token
    :return: HttpResponse obj or HttpResponseRedirect obj
    """
    if not request.user.is_valid and \
            request.user.valid_account(token.encode(encoding="ascii")):
        msg = {
            "validation": _("You have confirmed your account.")
        }
        return render(request, 'users/validate.html', msg)
    else:
        msg = {
            "expiration": "This link used to confirm your account is expired "
                          "or invalid."
        }
        return render(request, 'users/fail_to_validate.html', msg)


@login_required
def resend_email_view(request):
    """
    When the token is expired, allow user to resend activate link with a new
    token.
    :param request: HttpRequest object
    :return: HttpResponse
    """
    if request.user.is_valid:
            # if user has activated his/her account
            return render(request, 'index.html')
    elif request.user.is_active:
        # if user did not activate his/her account, then resend the email
        # including the token
        token = request.user.generate_valid_token()
        notify_user(request=request, token=token)
        msg = {
            "notification": _("The email including token has resent to you.")
        }
        return render(request, "users/resend_ok.html", msg)
    else:
        # if user is a blocked user, redirect to homepage
        return HttpResponseRedirect(reverse("article:index"))


def login_view(request):
    if request.method == 'POST':
        next_url = request.GET.get('next')
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is None:
                return render(request,
                              'users/login.html',
                              {"form": UserLoginForm(),
                               "status": "This user does not exists."}
                              )
            elif user.is_active or user.is_valid:
                login(request, user)
                if next_url is not None:
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect(reverse('article:index'))
            else:
                msg = {
                    "invalidation": "This account was banned. It can't not be \
                                    used to login this site."

                }
                return render(request, "users/blocked.html", msg)
    form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('article:index'))


@login_required
def password_reset_request(request):
    pass


@login_required
def password_reset(request):
    pass

