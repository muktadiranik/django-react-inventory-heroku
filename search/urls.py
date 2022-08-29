from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.Index.as_view(), name="search-index"),
    path("category/<str:pk>/",
         views.CategoryProduct.as_view(), name="category"),
    path("product/<str:pk>/", views.ProductDetails.as_view(), name="product")
]
