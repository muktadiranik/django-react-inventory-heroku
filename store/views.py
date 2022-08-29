from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from rest_framework import filters
# Create your views here.
from .serializers import CategorySerializer, HistorySerializer, ProductFileSerializer, ProductSerializer, ProductImageSerializer, SimpleHistorySerializer, SummarizeCategorySerializer, SummarizeProductSerializer
from .models import Category, History, Product, ProductFile, ProductImage


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs["category_pk"]).order_by("-updated_at")

    def get_serializer_context(self):
        return {"category_id": self.kwargs["category_pk"], "request": self.request}


class HistoryViewSet(ModelViewSet):
    serializer_class = HistorySerializer
    http_method_names = ["get", "post"]

    def get_queryset(self):
        return History.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"]}


class SimpleHistoryViewSet(ModelViewSet):
    serializer_class = SimpleHistorySerializer
    http_method_names = ["get", "delete"]
    filter_backends = [filters.SearchFilter]
    search_fields = ["$product__title"]

    def get_queryset(self):
        return History.objects.select_related("product").all()


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"], "request": self.request}

    def create(self, request, *args, **kwargs):
        data = {}
        images = request.FILES.getlist("image")

        serializer = self.serializer_class(
            data=data,
            context={
                "product_id": self.kwargs["product_pk"],
                "request": self.request,
                "images": images
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,  status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductFileViewSet(ModelViewSet):
    serializer_class = ProductFileSerializer

    def get_queryset(self):
        return ProductFile.objects.filter(product_id=self.kwargs["product_pk"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_pk"], "request": self.request}

    def create(self, request, *args, **kwargs):
        data = {}
        files = request.FILES.getlist("file")

        serializer = self.serializer_class(
            data=data,
            context={
                "product_id": self.kwargs["product_pk"],
                "request": self.request,
                "files": files
            }
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SummarizeCategoryViewSet(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = SummarizeCategorySerializer
    queryset = Category.objects.prefetch_related("product_set").all()


class SummarizeProductViewSet(ModelViewSet):
    http_method_names = ["get"]
    serializer_class = SummarizeProductSerializer

    def get_queryset(self):
        return Product.objects.filter(category_id=self.kwargs["category_pk"])
