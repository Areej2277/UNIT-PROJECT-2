from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from .forms import CustomUserCreationForm, EditProfileForm


# Create your views here.

#  Register a new user
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

#  login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

# logout
def user_logout(request):
    logout(request)
    return redirect('home')

# View profile
@login_required
def profile(request):
    user_ideas = request.user.idea_set.all()  
    return render(request, 'users/profile.html', {'user_ideas': user_ideas})

# Edit profile
@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = EditProfileForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('users:profile')

    else:
        user_form = EditProfileForm(instance=request.user)

    return render(request, 'users/edit_profile.html', {'user_form': user_form})