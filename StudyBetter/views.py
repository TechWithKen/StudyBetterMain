from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os
from StudyBetter.filemanipulation import get_content
from StudyBetter.machinemodel import make_prediction
from django.views.decorators.http import require_POST

def index(request):
    return render(request, "studybetterapp/index.html")

def dashboard(request): 
    return render(request, 'studybetterapp/dashboard.html')


def upload(request):
    
    if request.method == 'POST' and request.FILES:
        course_material = request.FILES.get('courseMaterial')
        past_questions = request.FILES.get('pastQuestions')
        course_material_string = get_content(course_material)
        past_questions_string = get_content(past_questions)

        if course_material and past_questions:
            result_text = make_prediction(past_questions_string, course_material_string)
            return render(request, 'studybetterapp/upload.html', {
                'sucess_message': 'Successful entry',
                'result_text': result_text
            })
        else:
            return render(request, 'studybetterapp/upload.html', {
                'error_message': 'Please upload both the course material and past questions.'
            })

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request, 'Invalid credentials')
    
    return render(request, 'studybetterapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')