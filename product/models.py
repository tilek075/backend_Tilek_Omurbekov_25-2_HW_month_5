from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(default=0.0)

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)

    def __str__(self):
        return self.text
