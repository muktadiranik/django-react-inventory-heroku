from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()

# store/categories/{category_pk}/
router.register("categories", views.CategoryViewSet, basename="categories")

# store/categories-summary/{category_pk}/
router.register("categories-summary",
                views.SummarizeCategoryViewSet, basename="categories-summary")


router.register("histories", views.SimpleHistoryViewSet, basename="histories")


# store/categories/{category_pk}/products/{product_pk}/
category_router = routers.NestedSimpleRouter(
    router, "categories", lookup="category")

category_router.register("products", views.ProductViewSet,
                         basename="category-products")

# store/categories-summary/{category_pk}/products-summary/{product_pk}/
category_summary_router = routers.NestedSimpleRouter(
    router, "categories-summary", lookup="category"
)

category_summary_router.register(
    "products-summary", views.SummarizeProductViewSet, basename="products-summary")


# store/{category_pk}/products/{product_pk}/images/{pk}/
# store/{category_pk}/products/{product_pk}/files/{pk}/
# store/{category_pk}/products/{product_pk}/histories/{pk}/
product_router = routers.NestedSimpleRouter(
    category_router, "products", lookup="product")

product_router.register(
    "images", views.ProductImageViewSet, basename="product-images")
product_router.register(
    "files", views.ProductFileViewSet, basename="product-files")
product_router.register(
    "histories", views.HistoryViewSet, basename="product-histories")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(category_router.urls)),
    path("", include(product_router.urls)),
    path("", include(category_summary_router.urls)),
]
