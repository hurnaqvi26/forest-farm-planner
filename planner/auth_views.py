from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from planner_core.sns_helper import subscribe_user_email


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
            return render(
                request,
                "accounts/register.html",
                {"error": "Passwords do not match"},
            )

        # Create the Django user
        user = User.objects.create_user(username=uname, email=email, password=pwd1)

        # Subscribe this email to SNS topic
        # (user must confirm subscription via email once)
        subscribe_user_email(email)

        # Optionally log them in after registration
        # login(request, user)

        return redirect("/")

    return render(request, "accounts/register.html")


def logout_view(request):
    logout(request)
    return redirect("/")
