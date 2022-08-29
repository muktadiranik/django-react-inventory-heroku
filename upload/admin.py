from django.contrib import admin
from .models import Category, Image, File

# Register your models here.


class ImageAdmin(admin.TabularInline):
    model = Image
    min_num = 1
    extra = 0


class FileAdmin(admin.TabularInline):
    model = File
    min_num = 1
    extra = 0


@admin.register(Category)
class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at", "updated_at"]
    inlines = [ImageAdmin, FileAdmin]
    list_display = ["title", "created_at", "updated_at"]
    fields = ["title"]
    list_per_page = 10
