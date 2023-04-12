from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, ProductValidateSerializer,\
    CategoryValidateSerializer, ReviewValidateSerializer
from product.models import Product, Category, Review
from rest_framework import status


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(instance=products, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'errors': serializer.errors})
        category_id = serializer.validated_data.get('category_id')
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        product = Product.objects.create(category_id=category_id, title=title, description=description, price=price)
        product.save()
        return Response(data=ProductSerializer(product).data)


@api_view(['GET', 'DELETE', 'PUT'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product.category_id = serializer.validated_data.get('category_id')
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.save()
        return Response(data=ProductSerializer(product).data)


@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name')
        category = Category.objects.create(name=name)
        category.save()
        return Response(data=CategorySerializer(category).data)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Category not found!'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(data=CategorySerializer(category).data)


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product_id = serializer.validated_data.get('product_id')
        text = serializer.validated_data.get('text')
        rating = serializer.validated_data.get('rating')
        review = Review.objects.create(product_id=product_id, text=text, rating=rating)
        review.save()
        return Response(data=ReviewSerializer(review).data)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Product.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'},
                        status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReviewSerializer(review)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.product_id = serializer.validated_data.get('product_id')
        review.text = serializer.validated_data.get('text')
        review.rating = serializer.validated_data.get('rating')
        review.save()
        return Response(data=ReviewSerializer(review).data)


@api_view(['GET'])
def product_reviews_api_view(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(data=serializer.data)
