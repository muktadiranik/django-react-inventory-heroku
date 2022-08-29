from django.contrib import admin
from .models import Category, Product
# Register your models here.

admin.site.register(Category)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]
    list_display = ["title", "category"]
    fields = ["title", "category", "description",
              "inventory", "unit_price", "image"]
    list_per_page = 10
