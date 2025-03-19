from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile

# Register a new user
def register(request: HttpRequest):
    if request.method == "POST":
        try:
            with transaction.atomic():
                username = request.POST["username"]
                password = request.POST["password"]
                confirm_password = request.POST["password2"]
                email = request.POST["email"]
                first_name = request.POST["first_name"]
                last_name = request.POST["last_name"]
                user_type = request.POST["user_type"]  # # Extract the account type

                
                if password != confirm_password:
                    messages.error(request, "Passwords do not match.", "alert-danger")
                    return render(request, "users/register.html")

                
                new_user = User.objects.create_user(
                    username=username, 
                    password=password, 
                    email=email, 
                    first_name=first_name, 
                    last_name=last_name
                )
                new_user.save()

                # Create a user profile based on the account type
                profile = Profile.objects.create(
                    user=new_user,
                    user_type=user_type,
                    about=request.POST.get("about", ""),
                    avatar=request.FILES.get("avatar", "images/avatars/avatar.webp")
                )

            messages.success(request, "Account created successfully!", "alert-success")
            return redirect("users:login")

        except IntegrityError:
            messages.error(request, "Username already taken, please try another.", "alert-danger")
        except Exception as e:
            messages.error(request, "Error creating account, please try again.", "alert-danger")
            print(f"Error in register view: {e}")

    return render(request, "users/register.html")


# # User login 
def user_login(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            return redirect(request.GET.get("next", "home"))
        else:
            messages.error(request, "Invalid username or password", "alert-danger")

    return render(request, "users/login.html")


# Log the user out
def user_logout(request: HttpRequest):
    logout(request)
    messages.success(request, "Logged out successfully", "alert-warning")
    return redirect("home")


#View profile
@login_required(login_url='/users/login/')
def profile(request: HttpRequest):
    return render(request, "users/profile.html", {"user": request.user})



@login_required(login_url='/users/login/')
def edit_profile(request: HttpRequest):
    if request.method == "POST":
        try:
            with transaction.atomic():
                user = request.user
                user.first_name = request.POST["first_name"]
                user.last_name = request.POST["last_name"]
                user.email = request.POST["email"]
                user.save()


                profile = user.profile
                profile.about = request.POST.get("about", "")

                if "avatar" in request.FILES:
                    profile.avatar = request.FILES["avatar"]

                profile.save()

            messages.success(request, "Profile updated successfully!", "alert-success")
            return redirect("users:profile")

        except Exception as e:
            messages.error(request, "Couldn't update profile, please try again.", "alert-danger")
            print(f"Error in edit_profile view: {e}")

    return render(request, "users/edit_profile.html", {"user": request.user})