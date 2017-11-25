from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from users.models import User
from users.forms import UserLoginForm, UserRegisterForm, \
                        PasswordResetForm, PasswordResetRequestForm


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = authenticate(request, email=email, password=password)
            except User.DoesNotExist:
                return HttpResponseRedirect(reverse('users:login'))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('article:index'))
    form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('article:index'))


def register(request):
    form = UserRegisterForm()
    return render(request, 'users/registration.html', {'form', form})


@login_required
def password_reset_request(request):
    pass


@login_required
def password_reset(request):
    pass

