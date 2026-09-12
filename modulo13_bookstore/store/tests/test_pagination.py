from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Category


class PaginationTests(APITestCase):
    def setUp(self):
        for index in range(12):
            Category.objects.create(
                name=f"Categoria {index:02d}",
                description=f"Descrição {index:02d}",
            )

    def test_default_pagination_returns_five_items(self):
        response = self.client.get(reverse("category-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIsNone(response.data["previous"])
        self.assertIsNotNone(response.data["next"])

    def test_second_page_returns_next_five_items(self):
        response = self.client.get(reverse("category-list"), {"page": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertIsNotNone(response.data["previous"])
        self.assertIsNotNone(response.data["next"])

    def test_page_size_can_be_customized_up_to_ten(self):
        response = self.client.get(reverse("category-list"), {"page_size": 10})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

    def test_page_size_respects_maximum_limit(self):
        response = self.client.get(reverse("category-list"), {"page_size": 100})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
