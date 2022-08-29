from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.db.transaction import atomic
from .models import Category, History, Product, ProductImage, ProductFile


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "title",  "created_at", "updated_at"]


class ProductImageSerializer(ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "image"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        images = self.context["images"]

        image_list = [ProductImage(
            product_id=product_id,
            image=image
        ) for image in images]

        instance = ProductImage.objects.bulk_create(image_list)

        return instance


class ProductFileSerializer(ModelSerializer):
    class Meta:
        model = ProductFile
        fields = ["id", "file"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        files = self.context["files"]

        file_list = [ProductFile(
            product_id=product_id,
            file=file
        ) for file in files]

        instance = ProductFile.objects.bulk_create(file_list)

        return instance


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "description", "created_at",
                  "updated_at", "inventory", "unit_price", "image"]

    def create(self, validated_data):
        category_id = self.context["category_id"]

        instance = Product.objects.create(
            category_id=category_id,
            **validated_data
        )

        return instance


class SimpleProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "image"]


class HistorySerializer(ModelSerializer):
    class Meta:
        model = History
        fields = ["id", "created_at", "quantity", "history_type"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        quantity = validated_data["quantity"]
        history_type = validated_data["history_type"]
        product = Product.objects.get(pk=product_id)

        with atomic():
            if history_type == "O":
                if quantity < product.inventory:
                    instance = History.objects.create(
                        product_id=product_id,
                        **validated_data)
                    product.inventory -= quantity
                    product.save()
                    return instance

                elif quantity == product.inventory:
                    instance = History.objects.create(
                        product_id=product_id,
                        **validated_data)
                    product.delete()
                    return instance

                else:
                    raise serializers.ValidationError(
                        "Quantity should be less than or equal product inventory")

            elif history_type == "I":
                instance = History.objects.create(
                    product_id=product_id,
                    **validated_data)
                product.inventory += quantity
                product.save()

                return instance


class SimpleHistorySerializer(ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = History
        fields = ["id", "product", "created_at", "quantity", "history_type"]


class SummarizeCategorySerializer(ModelSerializer):
    product_count = serializers.SerializerMethodField(
        method_name="get_product_count")

    class Meta:
        model = Category
        fields = ["id", "title", "product_count"]

    def get_product_count(self, category):
        return category.product_set.count()


class SummarizeProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "inventory", "unit_price"]
