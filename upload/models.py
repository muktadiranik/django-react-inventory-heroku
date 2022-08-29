from django.db import models


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title


class Image(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="upload/products/images/", null=True, blank=True)

    def __str__(self) -> str:
        return str(self.image)


class File(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    file = models.FileField(
        upload_to="upload/products/files/", null=True, blank=True)

    def __str__(self) -> str:
        return str(self.file)
