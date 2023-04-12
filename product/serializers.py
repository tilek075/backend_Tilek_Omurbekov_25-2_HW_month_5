from rest_framework import serializers
from product.models import Product, Category, Review
from rest_framework.exceptions import ValidationError


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


class ReviewValidateSerializer(serializers.Serializer):
    text = serializers.CharField(min_length=3, max_length=400)
    rating = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()

    def validate_product_id(self, product_id):
        try:
            Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError(f'Director with id ({product_id}) not found!')
        return product_id


class CategoryValidateSerializer(serializers.Serializer):
   name = serializers.CharField(min_length=3, max_length=20)


class ProductValidateSerializer(serializers.Serializer):
    category_id = serializers.IntegerField()
    title = serializers.CharField(min_length=3, max_length=100)
    description = serializers.CharField(required=False, default='No text')
    price = serializers.FloatField(min_value=0.1, max_value=9999999.99, default=0.0)

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError(f'Director with id ({category_id}) not found!')
        return category_id
