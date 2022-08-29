from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    image = models.ImageField(upload_to="products/", null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class History(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    HISTORY_TYPE_CHOICE_IN = "I"
    HISTORY_TYPE_CHOICE_OUT = "O"
    HISTORY_TYPE_CHOICES = [
        (HISTORY_TYPE_CHOICE_IN, "IN"),
        (HISTORY_TYPE_CHOICE_OUT, "OUT")
    ]

    history_type = models.CharField(max_length=1, choices=HISTORY_TYPE_CHOICES)

    def __str__(self) -> str:
        return str(self.product)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="products/images/", null=True, blank=True)


class ProductFile(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="products/files/", null=True, blank=True)
