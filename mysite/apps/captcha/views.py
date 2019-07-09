from django.core.cache import cache
from django.views.generic import View, TemplateView
from django.http.response import JsonResponse

from .captcha import Captcha


class CaptchaView(View):
    def dispatch(self, request, *args, **kwargs):
        return super(CaptchaView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        cached_time = 30 * 60  # a half of an hour
        captcha = Captcha()
        text, captcha_img = captcha.generate_captcha()
        cache.set(text, text, cached_time)
        return JsonResponse(
            {"captchaAddress": captcha_img, "status": 0, "message": "success"}
        )

    def http_method_not_allowed(self, request, *args, **kwargs):
        HTTP_405_METHOD_NOT_ALLOWED = 405
        return JsonResponse(
            {"capchaAddress": None, "staus": 1, "message": "Not allowed"},
            status=HTTP_405_METHOD_NOT_ALLOWED,
        )
