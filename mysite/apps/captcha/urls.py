from django.conf.urls import url

from .views import CaptchaView

app_name = "captcha"

urlpatterns = [url(r"^captcha/$", CaptchaView.as_view(), name="get_captcha")]
