from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


def login_view(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        pwd = request.POST.get("password")
        user = authenticate(username=uname, password=pwd)

        if user:
            login(request, user)
            return redirect("/dashboard/")

        return render(request, "accounts/login.html", {"error": True})

    return render(request, "accounts/login.html")


def register_view(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        email = request.POST.get("email")
        pwd1 = request.POST.get("password1")
        pwd2 = request.POST.get("password2")

        if pwd1 != pwd2:
            return render(request, "accounts/register.html", {"error": "Passwords do not match"})

        if User.objects.filter(username=uname).exists():
            return render(request, "accounts/register.html", {"error": "Username already taken"})

        User.objects.create_user(username=uname, email=email, password=pwd1)
        return redirect("/login/")

    return render(request, "accounts/register.html")


def logout_view(request):
    logout(request)
    return redirect("/login/")
