from rest_framework import serializers
from product.models import Product, Category, Review


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title price category'.split()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'name'.split()


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'text'.split()
