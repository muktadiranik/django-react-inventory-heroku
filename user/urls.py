from django.urls import path
from . import views

urlpatterns = [
    path("registration/", views.UserRegistration.as_view(), name="registration"),
    path("", views.Index.as_view(), name="index"),
    path("login/", views.UserLogin.as_view(), name="login"),
    path("logout/", views.UserLogout.as_view(), name="logout"),
]
