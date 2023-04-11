from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.title


STAR_CHOICES = ((iterator_, '* ' * iterator_) for iterator_ in range(1, 6))


class Review(models.Model):
    text = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(default=5, choices=STAR_CHOICES)

    def __str__(self):
        return f'{self.rating} star review for {self.product}'
