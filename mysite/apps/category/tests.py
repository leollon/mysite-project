from django.test import Client as HTTPClient
from django.test import TestCase


class TestCategory(TestCase):

    def setUp(self) -> None:
        self.http_client = HTTPClient()

    def test_categtories_list(self):

        response = self.http_client.get("/api/v1/categories/")
        self.assertEqual(response.status_code, 200)

        response = self.http_client.post("/api/v1/categories/", data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.put("/api/v1/categories/", data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.patch("/api/v1/categories/", data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.delete("/api/v1/categories/", data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.get("/api/v1/categories/hello-world/")
        self.assertEqual(response.status_code, 404)

        response = self.http_client.post("/api/v1/categories/hello-world/", data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 404)

        response = self.http_client.put("/api/v1/categories/hello-world/", data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 404)

        response = self.http_client.patch("/api/v1/categories/hello-world/", data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 404)

        response = self.http_client.delete("/api/v1/categories/hello-world/", data={"name": "test_catetory"})
        self.assertEqual(response.status_code, 404)

    def test_get_categorized_article_list(self):

        response = self.http_client.get("/api/v1/categories/Sams-Teach-yourself-TCPIP-in-24-hours/articles/")
        assert len(response.data.get("results")) >= 0
        self.assertEqual(response.status_code, 200)

        response = self.http_client.get("/api/v1/categories/undefined/articles/")  # unknown category name
        self.assertEqual(response.data.get("results"), [])
        assert len(response.data.get("results")) >= 0
        self.assertEqual(response.status_code, 200)

        response = self.http_client.get("/api/v1/categories/undefined/articles/", data={"name": "WhatDoUThink"})
        self.assertEqual(response.status_code, 200)

        response = self.http_client.post("/api/v1/categories/", data={"name": "WhatDoUThink"})
        self.assertEqual(response.status_code, 405)

        response = self.http_client.post("/api/v1/categories/", data={"name": "WhatDoUThink"})
        self.assertEqual(response.status_code, 405)
