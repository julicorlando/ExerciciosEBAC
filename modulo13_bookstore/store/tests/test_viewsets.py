from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from store.models import Category, Order, Product


class ViewSetTests(APITestCase):
    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            username="julio",
            password="SenhaForte123!",
            email="julio@example.com",
        )
        self.token = Token.objects.create(user=self.user)

        self.category = Category.objects.create(
            name="Programação",
            description="Livros de desenvolvimento de software",
        )
        self.other_category = Category.objects.create(
            name="Banco de dados",
            description="Livros de bancos relacionais e NoSQL",
        )

        self.product = Product.objects.create(
            name="Django REST Framework",
            description="Construção de APIs REST com Django",
            price="89.90",
            stock=10,
        )
        self.product.categories.add(self.category)

        self.other_product = Product.objects.create(
            name="PostgreSQL na prática",
            description="Fundamentos de PostgreSQL",
            price="69.90",
            stock=5,
        )
        self.other_product.categories.add(self.other_category)

        self.order = Order.objects.create(
            user=self.user,
            customer_name="Julio Orlando",
            customer_email="julio@example.com",
        )
        self.order.products.add(self.product)

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_category_viewset_full_crud(self):
        list_url = reverse("category-list")

        list_response = self.client.get(list_url)
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.data["results"]), 2)
        self.assertEqual(list_response.data["count"], 2)

        create_response = self.client.post(
            list_url,
            {"name": "DevOps", "description": "Automação e infraestrutura"},
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        category_id = create_response.data["id"]
        detail_url = reverse("category-detail", args=[category_id])

        retrieve_response = self.client.get(detail_url)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.data["name"], "DevOps")

        update_response = self.client.patch(
            detail_url,
            {"description": "CI/CD, containers e infraestrutura"},
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            update_response.data["description"],
            "CI/CD, containers e infraestrutura",
        )

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Category.objects.filter(pk=category_id).exists())

    def test_product_list_represents_categories_without_authentication(self):
        response = self.client.get(reverse("product-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

        product_data = next(
            item for item in response.data["results"] if item["id"] == self.product.id
        )
        self.assertEqual(product_data["categories"][0]["id"], self.category.id)
        self.assertEqual(
            product_data["categories"][0]["name"],
            self.category.name,
        )

    def test_product_viewset_creates_product_with_categories(self):
        response = self.client.post(
            reverse("product-list"),
            {
                "name": "APIs com Python",
                "description": "Projeto de APIs profissionais",
                "price": "59.90",
                "stock": 7,
                "category_ids": [self.category.id, self.other_category.id],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product = Product.objects.get(pk=response.data["id"])
        self.assertEqual(product.categories.count(), 2)
        self.assertEqual(len(response.data["categories"]), 2)

    def test_product_viewset_rejects_missing_categories(self):
        response = self.client.post(
            reverse("product-list"),
            {
                "name": "Produto sem categoria",
                "price": "29.90",
                "stock": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("category_ids", response.data)

    def test_product_viewset_retrieve_update_and_delete(self):
        detail_url = reverse("product-detail", args=[self.product.id])

        retrieve_response = self.client.get(detail_url)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.data["name"], self.product.name)

        update_response = self.client.patch(
            detail_url,
            {"stock": 25},
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 25)

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Product.objects.filter(pk=self.product.id).exists())

    def test_order_viewset_creates_order_with_products(self):
        self.authenticate()
        response = self.client.post(
            reverse("order-list"),
            {
                "customer_name": "Maria Silva",
                "customer_email": "maria@example.com",
                "status": Order.Status.PENDING,
                "product_ids": [self.product.id, self.other_product.id],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(pk=response.data["id"])
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.products.count(), 2)
        self.assertEqual(len(response.data["products"]), 2)

    def test_order_viewset_rejects_invalid_email(self):
        self.authenticate()
        response = self.client.post(
            reverse("order-list"),
            {
                "customer_name": "Cliente inválido",
                "customer_email": "email-invalido",
                "product_ids": [self.product.id],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("customer_email", response.data)

    def test_order_viewset_retrieve_update_and_delete(self):
        self.authenticate()
        detail_url = reverse("order-detail", args=[self.order.id])

        retrieve_response = self.client.get(detail_url)
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_response.data["customer_name"], "Julio Orlando")
        self.assertEqual(retrieve_response.data["products"][0]["id"], self.product.id)

        update_response = self.client.patch(
            detail_url,
            {"status": Order.Status.PAID},
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, Order.Status.PAID)

        delete_response = self.client.delete(detail_url)
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Order.objects.filter(pk=self.order.id).exists())
