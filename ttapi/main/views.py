from django.shortcuts import render , redirect
from django.http import HttpResponse, JsonResponse
from .nwuapi import time_table_api
from django.contrib.auth import authenticate, login as auth_login , logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from datetime import datetime

date_p = ""

def check_date(modules, date_pp):
    global date_p
    if date_pp == "":
        # Get today's date
        today_date = datetime.now().date()
    else:
        today_date = datetime.strptime(date_pp, "%Y-%m-%d").date()
        date_pp = ""
    # Create a new list to store modules that match today's date
    filtered_modules = []
    # Check if the given date matches today's date
    for module in modules:
        date_string = module['start']
        date_string = date_string.split("T")[0]
        given_date = datetime.strptime(date_string, "%Y-%m-%d").date()
        if today_date == given_date:
            filtered_modules.append(module)
    return filtered_modules

        
@login_required
def delete_account(request):
    if request.method == 'POST':
        # Confirm that the user really wants to delete their account
        if request.POST.get('confirm_delete'):
            # Delete the user's account
            request.user.delete()
            # Logout the user after deleting the account
            logout(request)
            return redirect(signup)  # Redirect to home page or any other appropriate page after deletion
    return render(request, 'profile.html')  # Render a confirmation template

def date_picked(request):
    global date_p
    if request.method == 'POST':
        date = request.POST.get('date')
        date_p = date
        print(date)
        return redirect(home)

def logout_view(request):
    logout(request)
    return redirect(login)  # Redirect to login page after logout

def profile_view(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(author=request.user)
        if request.method == 'POST' and 'module_code' in request.POST:
            module_code = request.POST.get('module_code')
            module_code = module_code.replace(" ", "")
            crawler = time_table_api(module_code_group= module_code)
            if crawler.check_module_code(module_code_group=module_code) == True:
                profile.module_code = module_code
                profile.save()
                return redirect(home)
            elif crawler.check_module_code(module_code_group=module_code) == None:
                return render(request, 'profile.html', {'profile': profile, 'error_message': 'Invalid course code','user': request.user})
        return render(request, 'profile.html', {'profile': profile,'user': request.user})
    else:
        return redirect(login)

def home(request):
    current_date = str(datetime.now().date())
    # Check if the user is authenticated
    if request.user.is_authenticated:
        profile = Profile.objects.get(author=request.user)
        module_code = profile.module_code
        
        # Check if the user has a module code
        if module_code == '':
            return redirect(profile_view)
        
        # Get the time table
        time_table = time_table_api(module_code, date_p)
        size_of_table = time_table.return_module_size()
        modules = time_table.return_modules()
        modules = check_date(modules, date_p)
        if date_p == "":
            current_date = str(datetime.now().date())
        else:
            current_date = date_p
        return render(request, 'index.html', {'modules': modules, 'current_date':current_date})
    return render(request, 'index.html', {'current_date':current_date})

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
    