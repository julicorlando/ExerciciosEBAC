from decimal import Decimal

from django.test import TestCase

from store.models import Category, Order, Product
from store.serializers import CategorySerializer, OrderSerializer, ProductSerializer


class CategorySerializerTests(TestCase):
    def test_accepts_valid_data_and_creates_category(self):
        serializer = CategorySerializer(
            data={"name": "Ficção", "description": "Livros de ficção"}
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        category = serializer.save()
        self.assertEqual(category.name, "Ficção")

    def test_rejects_missing_required_name(self):
        serializer = CategorySerializer(data={"description": "Sem nome"})

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


class ProductSerializerTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Tecnologia", description="Livros de tecnologia"
        )

    def test_accepts_valid_data_and_creates_product_with_category(self):
        serializer = ProductSerializer(
            data={
                "name": "Django REST Framework",
                "description": "API REST com Django",
                "price": "79.90",
                "stock": 8,
                "category_ids": [self.category.pk],
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        product = serializer.save()
        self.assertEqual(product.categories.count(), 1)
        self.assertEqual(product.categories.first(), self.category)

    def test_rejects_missing_required_name(self):
        serializer = ProductSerializer(
            data={
                "price": "59.90",
                "stock": 2,
                "category_ids": [self.category.pk],
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)

    def test_rejects_invalid_negative_price(self):
        serializer = ProductSerializer(
            data={
                "name": "Produto inválido",
                "price": "-10.00",
                "stock": 1,
                "category_ids": [self.category.pk],
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("price", serializer.errors)

    def test_returns_expected_fields_and_nested_category(self):
        product = Product.objects.create(
            name="Python para APIs",
            description="Livro de APIs",
            price=Decimal("89.90"),
            stock=4,
        )
        product.categories.add(self.category)

        data = ProductSerializer(product).data

        self.assertEqual(
            set(data.keys()),
            {"id", "name", "description", "price", "stock", "categories"},
        )
        self.assertEqual(data["categories"][0]["id"], self.category.pk)
        self.assertEqual(data["categories"][0]["name"], "Tecnologia")


class OrderSerializerTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Backend")
        self.product = Product.objects.create(
            name="Django Avançado",
            price=Decimal("99.90"),
            stock=5,
        )
        self.product.categories.add(self.category)

    def test_accepts_valid_data_and_creates_order_with_products(self):
        serializer = OrderSerializer(
            data={
                "customer_name": "Julio Orlando",
                "customer_email": "julio@example.com",
                "status": Order.Status.PENDING,
                "product_ids": [self.product.pk],
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        order = serializer.save()
        self.assertEqual(order.products.count(), 1)
        self.assertEqual(order.products.first(), self.product)

    def test_rejects_invalid_email(self):
        serializer = OrderSerializer(
            data={
                "customer_name": "Julio Orlando",
                "customer_email": "email-invalido",
                "product_ids": [self.product.pk],
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("customer_email", serializer.errors)

    def test_rejects_missing_products(self):
        serializer = OrderSerializer(
            data={
                "customer_name": "Julio Orlando",
                "customer_email": "julio@example.com",
            }
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("product_ids", serializer.errors)

    def test_returns_expected_fields_and_nested_products(self):
        order = Order.objects.create(
            customer_name="Julio Orlando",
            customer_email="julio@example.com",
        )
        order.products.add(self.product)

        data = OrderSerializer(order).data

        self.assertEqual(
            set(data.keys()),
            {
                "id",
                "customer_name",
                "customer_email",
                "status",
                "products",
                "created_at",
            },
        )
        self.assertEqual(data["products"][0]["id"], self.product.pk)
        self.assertEqual(
            data["products"][0]["categories"][0]["name"], "Backend"
        )
