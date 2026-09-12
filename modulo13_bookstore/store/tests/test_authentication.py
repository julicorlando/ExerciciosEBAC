from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from store.models import Category, Order, Product


class TokenAuthenticationTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="julio",
            password="SenhaForte123!",
            email="julio@example.com",
        )
        self.other_user = user_model.objects.create_user(
            username="maria",
            password="OutraSenha123!",
            email="maria@example.com",
        )
        self.token = Token.objects.create(user=self.user)
        self.other_token = Token.objects.create(user=self.other_user)

        category = Category.objects.create(name="Programação")
        self.product = Product.objects.create(
            name="Django REST Framework",
            price="89.90",
            stock=10,
        )
        self.product.categories.add(category)

        self.order = Order.objects.create(
            user=self.user,
            customer_name="Julio Orlando",
            customer_email="julio@example.com",
        )
        self.order.products.add(self.product)

        self.other_order = Order.objects.create(
            user=self.other_user,
            customer_name="Maria Silva",
            customer_email="maria@example.com",
        )
        self.other_order.products.add(self.product)

    def authenticate(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_product_endpoint_remains_public(self):
        response = self.client.get(reverse("product-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_order_endpoint_requires_token(self):
        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_token_is_rejected(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token token-invalido")

        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_sees_only_own_orders(self):
        self.authenticate(self.token)

        response = self.client.get(reverse("order-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["id"], self.order.id)

    def test_user_cannot_retrieve_another_users_order(self):
        self.authenticate(self.token)

        response = self.client.get(
            reverse("order-detail", args=[self.other_order.id])
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_creation_associates_order_with_user(self):
        self.authenticate(self.token)

        response = self.client.post(
            reverse("order-list"),
            {
                "customer_name": "Novo Cliente",
                "customer_email": "novo@example.com",
                "product_ids": [self.product.id],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(pk=response.data["id"])
        self.assertEqual(order.user, self.user)

    def test_token_endpoint_returns_user_token(self):
        response = self.client.post(
            reverse("api-token"),
            {"username": "julio", "password": "SenhaForte123!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token"], self.token.key)
