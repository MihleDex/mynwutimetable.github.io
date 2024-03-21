from django.shortcuts import render , redirect
from django.http import HttpResponse
from .nwuapi import time_table_api
from django.contrib.auth import authenticate, login as auth_login , logout
from django.contrib.auth.models import User
from .models import Profile


def logout_view(request):
    logout(request)
    return redirect(login)  # Redirect to login page after logout

def profile_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(author=request.user)
        
        if request.method == 'POST':
            module_code = request.POST.get('module_code')
            profile.module_code = module_code
            profile.save()
            return redirect(profile_view)
        return render(request, 'profile.html', {'profile': profile,'user': request.user})
    else:
        return redirect(login)

def home(request):
    #return template
    return render(request, 'index.html', {'name': 'MyNwuTimeTable'})

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            # Check if the username is unique
            if User.objects.filter(username=username).exists():
                return render(request, 'signup.html', {'error_message': 'Username already exists'})

            # Create the user
            user = User.objects.create_user(username=username, password=password1)
            profile = Profile.objects.create(author=user, email=email)
            profile.save()
            auth_login(request, user)
            return redirect(home)  # Redirect to home page after successful registration
        else:
            return render(request, 'signup.html', {'error_message': 'Passwords do not match'})
    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect(home)  # Redirect to home page after login
        else:
            # Handle invalid login
            return render(request, 'login.html', {'error_message': 'Invalid login'})
    else:
        return render(request, 'login.html')
    