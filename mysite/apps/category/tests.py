import unittest

from django.test import Client as HTTPClient
from django.test import RequestFactory

from ..user.models import User


class TestCategory(unittest.TestCase):

    def setUp(self) -> None:
        self.http_client = HTTPClient()
        self.request_factory = RequestFactory()
        self.user = User.objects.get_or_create(
            username='test', email='email@test.com',
            password='test1234', user_permission=[
                "category.add_articlecategory", "category.view_articlecategory",
                "category.change_articlecategory", "category.delete_articlecategory"]
        )

    def test_get_categtories_list(self):
        response = self.http_client.get("/categories/")
        self.assertEqual(response.status_code, 200)
