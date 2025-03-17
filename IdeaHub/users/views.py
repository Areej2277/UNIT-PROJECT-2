from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import CustomUserCreationForm, EditProfileForm


# Register new user
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .forms import CustomUserCreationForm, EditProfileForm

# Register new user
def register(request: HttpRequest):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save(commit=False)
                    user.user_type = form.cleaned_data['user_type']
                    user.save()
                    user = authenticate(request, username=user.username, password=form.cleaned_data['password1'])
                    if user:
                        login(request, user)
                        messages.success(request, "Account created successfully!", "alert-success")
                        return redirect("home")

            except IntegrityError:
                messages.error(request, "Username already taken, please try another.", "alert-danger")
            except Exception as e:
                messages.error(request, "Error creating account, please try again.", "alert-danger")
                print(e)
    else:
        form = CustomUserCreationForm()

    return render(request, "users/register.html", {"form": form})


# User login
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


# Logout user
def user_logout(request: HttpRequest):
    logout(request)
    messages.success(request, "Logged out successfully", "alert-warning")
    return redirect("home")


# View profile
@login_required(login_url='/users/login/')  
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})


# Edit profile
@login_required(login_url='/users/login/')
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            if 'profile_picture' in request.FILES:
                request.user.profile_picture = request.FILES['profile_picture']
            user_form.save()
            messages.success(request, "Profile updated successfully!", "alert-success")
            return redirect('users:profile')

    else:
        user_form = EditProfileForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'user_form': user_form})