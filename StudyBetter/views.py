from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from django.db import IntegrityError  # remove it if you are not using it.
from django.contrib.auth.models import User

def index(request):
    return render(request, "studybetterapp/index.html")

def dashboard(request): 
    return render(request, 'studybetterapp/dashboard.html')

def upload(request):
    return render(request, 'studybetterapp/upload.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            # Authenticate the user without specifying the backend instance directly
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'studybetterapp/signup.html', {'error': 'Passwords do not match'})
    else:
        return render(request, 'studybetterapp/signup.html')



# Login view
def login_view(request):  # Renamed to avoid conflict
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Adjust URL pattern if needed
        else:
            messages.info(request, 'Invalid credentials')
    
    return render(request, 'studybetterapp/login.html')


# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')
