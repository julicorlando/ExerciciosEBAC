from rest_framework import serializers

from .models import Category, Order, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]
        read_only_fields = ["id"]


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        source="categories",
        many=True,
        queryset=Category.objects.all(),
        write_only=True,
        required=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "stock",
            "categories",
            "category_ids",
        ]
        read_only_fields = ["id"]


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    product_ids = serializers.PrimaryKeyRelatedField(
        source="products",
        many=True,
        queryset=Product.objects.all(),
        write_only=True,
        required=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_name",
            "customer_email",
            "status",
            "products",
            "product_ids",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
