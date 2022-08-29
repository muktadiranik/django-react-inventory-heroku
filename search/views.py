from django.shortcuts import render
from django.views import View
from django.db.models import Q
from .models import Category, Product

# Create your views here.


class Index(View):
    def get(self, request):
        search_keyword = request.GET.get("search_keyword")

        if search_keyword == None:
            products = Product.objects.select_related("category").all()
            categories = Category.objects.all()
        else:
            products = Product.objects.select_related(
                "category").filter(Q(title__icontains=search_keyword) |
                                   Q(category__title__icontains=search_keyword)
                                   )
            categories = Category.objects.filter(
                Q(title__icontains=search_keyword))

        return render(request, "search/index.html", {
            "products": products,
            "categories": categories,
        })


class CategoryProduct(View):
    def get(self, request, pk):
        products = Product.objects.select_related(
            "category").filter(category=pk)
        categories = Category.objects.all()

        return render(request, "search/index.html", {
            "products": products,
            "categories": categories,
        })


class ProductDetails(View):
    def get(self, request, pk):
        product = Product.objects.select_related("category").get(pk=pk)

        return render(request, "search/product.html", {
            "product": product,
        })
