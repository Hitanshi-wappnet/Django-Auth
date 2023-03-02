from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def home(request):
    return render(request, "base.html")


def registration(request):
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if User.objects.filter(username=username):
            messages.error(request, "User name already exists!Please try another")
            return redirect("/home/registration/")

        if User.objects.filter(email=email):
            messages.error(request, "Email already exists!Please try another")
            return redirect("/home/registration/")

        if password != confirm_password:
            messages.error(request, "Password and Confirm Password didn't match")
            return redirect("/home/registration/")

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request, "Your Registration is successful!!")
        return redirect("/home/login")

    return render(request, "registration.html")


def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "dashboard.html", {"name": fname})
        else:
            messages.error(request, "Your Username or Password is Wrong")
            return redirect("/home/login")

    return render(request, "login.html")


def signout(request):
    logout(request)
    messages.success(request, "You are successfully Logged out")
    return redirect("/home/")


def dashboard(request):
    return render(request, "dashboard.html")
