from django.test import SimpleTestCase, TestCase
from django.urls import reverse

from .captcha import Captcha


class TestCaptcha(SimpleTestCase):

    def setUp(self) -> None:
        self.captcha = Captcha()
        self.captcha_without_draw_line = Captcha(draw_lines=False)
        self.captcha_without_draw_points = Captcha(draw_points=False)
        self.captcha_with_draw_transform = Captcha(draw_transform=True)
        self.captcha_with_xy = Captcha(xy=(1, 2))

    def test_generate_captch(self):
        self.captcha.generate_captcha()
        self.captcha_without_draw_line.generate_captcha()
        self.captcha_with_draw_transform.generate_captcha()
        self.captcha_without_draw_points.generate_captcha()
        self.captcha_with_xy.generate_captcha()

        try:
            setattr(self.captcha, "_draw", None)
        except AttributeError:
            self.assertRaises(AttributeError)


class TestCaptchaAPIView(TestCase):

    def setUp(self) -> None:
        self.http_client = self.client_class()

    def test_get_captcha_success(self) -> None:
        response = self.http_client.get(reverse("api:captcha"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "message")
        self.assertContains(response, "captchaImgPath")
        self.assertContains(response, "CSRFToken")
        self.assertContains(response, "resultStatus")

    def test_http_method_not_allowed(self) -> None:

        response = self.http_client.post(
            reverse("api:captcha"),
            data={
                "captcha": "jijl83"
            })
        self.assertEqual(response.status_code, 405)
        self.assertContains(response, text=2, status_code=405)
        self.assertContains(response, text="Not allowed", status_code=405)
        self.assertContains(response, text="null", status_code=405)

        response = self.http_client.put(
            reverse("api:captcha"),
            data={
                "captcha": "jijl83"
            })
        self.assertEqual(response.status_code, 405)
        self.assertContains(response, text=2, status_code=405)
        self.assertContains(response, text="Not allowed", status_code=405)
        self.assertContains(response, text="null", status_code=405)

        response = self.http_client.options(
            reverse("api:captcha"),
            data={
                "captcha": "jijl83"
            })
        self.assertEqual(response.status_code, 405)

        response = self.http_client.head(
            reverse("api:captcha"),
            data={
                "captcha": "jijl83"
            })
        self.assertEqual(response.status_code, 405)
