from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from .forms import (PasswordResetForm, PasswordResetRequestForm, UserLoginForm,
                    UserRegisterForm)
from .models import User
from .utils import notify_user

email_related = getattr(settings, 'EMAIL_RELATED')
reg_notification_file = email_related.get('REG_NOTIFICATION_FILE')
pwd_change_notification_file = email_related.get(
    'PWD_CHANGE_NOTIFICATION_FILE')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'])
            user.set_password(form.cleaned_data['password1'])
            user.save()
            notify_user(
                request=request,
                url="/accounts/validate/",
                token=user.generate_valid_token(),
                subject="Confirm your account",
                filename=reg_notification_file)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            return render(request, 'user/register.html', {'form': form})
    else:
        form = UserRegisterForm()
        return render(request, 'user/register.html', {'form': form})


@login_required
def validate_view(request, token):
    """
    :param request: HttpRequest object
    :param token: user's activating token
    :return: HttpResponse obj or HttpResponseRedirect obj
    """
    if not request.user.is_valid and \
            request.user.valid_account(token.encode(encoding="ascii")):
        msg = {"validation": _("You have confirmed your account.")}
        return render(request, 'user/validate.html', msg)
    else:
        msg = {
            "expiration":
            "This link used to confirm your account is expired "
            "or invalid."
        }
        return render(request, 'user/expiration.html', msg)


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
        return render(request, 'article/index.html')
    elif request.user.is_active:
        # if user did not activate his/her account, then resend the email
        # including the token
        notify_user(
            request=request,
            url="/accounts/validate/",
            token=request.user.generate_valid_token(),
            subject="Confirm your account",
            filename=reg_notification_file)
        msg = {
            "notification": _("The email including token has resent to you.")
        }
        return render(request, "user/send_ok.html", msg)
    else:
        # if user is a blocked user, redirect to homepage
        return HttpResponseRedirect(reverse("articles:index"))


def login_view(request):
    if request.method == 'POST':
        next_url = request.GET.get('next')
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is None:
                return render(
                    request, 'user/login.html', {
                        "form": UserLoginForm(),
                        "status": "Username and Password mismatch."
                    })
            elif user.is_active or user.is_valid:
                login(request, user)
                if next_url is not None:
                    return HttpResponseRedirect(next_url)
                else:
                    return HttpResponseRedirect(reverse('user:dashboard'))
            else:
                msg = {
                    "invalidation":
                    "This account was banned. It can't not be \
                                    used to login this site."
                }
                return render(request, "user/blocked.html", msg)
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('user:dashboard'))
    form = UserLoginForm()
    return render(request, 'user/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('user:login'))


@login_required
def password_reset_request(request):
    if request.method == "POST":
        # send user email including the token
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            notify_user(
                request,
                url="/accounts/password_reset/",
                token=request.user.generate_email_token(),
                subject="Change Password",
                filename=pwd_change_notification_file)
            msg = {
                "notification": "The email including token has sent to you."
            }
            return render(request, "user/send_ok.html", msg)
        else:
            return render(request, "user/password_reset_request.html",
                          {"form": form})
    else:
        form = PasswordResetRequestForm()
        return render(request, "user/password_reset_request.html",
                      {"form": form})


@login_required
def password_reset(request, token):
    if request.method == "POST" and request.user.verify_email_token(token):
        form = PasswordResetForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password2'])
            request.user.save()
            return HttpResponseRedirect(reverse("user:login"))
        else:
            # bug：表单渲染后，页面未显示错误
            # why：PasswordResetForm自定义了__init__()，当post过来的时候，request.POST
            #     复制给了user，但是BaseForm的__init__()的data并没有数据接收到数据，
            #     默认值是None的，所以form是is not valid的
            # how：在PasswordResetForm类中定义的__init__方法多声明一个data参数，传参的时候
            #      一一对应地将参数传给方法中的参数
            # Result：Fixed
            return render(request, "user/password_reset.html", {"form": form})

    if request.user.verify_email_token(token):
        form = PasswordResetForm(request.user)
        return render(request, "user/password_reset.html", {"form": form})
    else:
        msg = {"expiration": _("The token is expired or invalid.")}
        return render(request, "user/expiration.html", msg)


@login_required
def dashboard(request):
    return render(request, "user/dashboard.html")
