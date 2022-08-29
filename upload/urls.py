from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="upload-index"),
    path("upload-images/", views.UploadImage.as_view(), name="upload-images"),
    path("upload-files/", views.UploadFile.as_view(), name="upload-files"),
    path("delete-category/<str:pk>/",
         views.DeleteCategory.as_view(), name="delete-category"),
    path("delete-image/<str:pk>/",
         views.DeleteImage.as_view(), name="delete-image"),
    path("delete-file/<str:pk>/",
         views.DeleteFile.as_view(), name="delete-file"),
    path("category-images-files/<str:pk>/",
         views.CategoryImageFile.as_view(), name="category-images-files"),
]
