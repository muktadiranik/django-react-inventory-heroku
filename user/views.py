from django.shortcuts import render, redirect
from django.views import View
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login, logout, authenticate
# Create your views here.
from .forms import RegisterUserForm


# both django-allauth authentication and Django's default authentication been implemented


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect("index")


class UserLogin(View):
    def get(self, request):
        return render(request, "user/login.html", {})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "user/login.html", {})


class UserRegistration(View):
    def get(self, request):
        form = RegisterUserForm()
        return render(request, "user/registration.html", {
            "form": form
        })

    def post(self, request):
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(
                request,
                username=username,
                password=password
            )

            login(request, user)

            return redirect("index")
        else:
            return render(request, "user/registration.html", {
                "form": form
            })


class Index(View):
    def get(self, request):

        return render(request, "user/index.html", {})
