from django.core.cache import cache
from django.views.generic import View
from django.views.generic.base import ContextMixin
from django.http.response import JsonResponse

from .captcha import Captcha


class CaptchaView(ContextMixin, View):
    http_method_names = ["get"]

    def get(self, request, *args, **kwargs):
        cached_time = 30 * 60  # a half of an hour
        captcha = Captcha()
        text, captcha_img_path, result_status, message = (
            captcha.generate_captcha()
        )
        cache.set(key=text, value=text, timeout=cached_time)
        return JsonResponse(
            {
                "captchaImgPath": captcha_img_path,
                "message": message,
                "resultStatus": result_status,
            }
        )

    def http_method_not_allowed(self, request, *args, **kwargs):
        HTTP_405_METHOD_NOT_ALLOWED = 405
        return JsonResponse(
            {
                "captchaImgPath": None,
                "message": "Not allowed",
                "resultStatus": 2,
            },
            status=HTTP_405_METHOD_NOT_ALLOWED,
        )
