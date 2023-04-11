from rest_framework import serializers
from product.models import Product, Category, Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text rating'.split()


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = 'id name products_count'.split()

    def get_products_count(self, obj):
        return obj.product_set.count()


class ProductSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = 'id title description price category reviews average_rating'.split()

    def get_average_rating(self, obj):
        reviews = Review.objects.filter(product=obj)
        if reviews:
            total = sum([review.rating for review in reviews])
            return total / len(reviews)
        else:
            return 0
