from django.shortcuts import render, HttpResponse,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse

def temp(request):
    return render(request,"home/temp.html",context={})

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard') 

    if request.method == 'POST':
        temp_email=request.POST.get('email')
        password=request.POST.get('pass1')
        
        email=temp_email.lower()
            
        try:
            verify_user=User.objects.get(email=email)    
        except:
            messages.error(request, 'No User found !')
            return redirect('home')
        
        try:
            tempuser=User.objects.get(email=email).username                  
            user=authenticate(request,username=tempuser,password=password)
        except:
            messages.error(request, 'Incorrect Password !')
            return redirect('home')
                  
        if user == None: 
            messages.error(request, 'No User Exists !')
            return redirect('home')
        
        if user.is_active:
            login(request,user)
            return redirect('home')
    return render(request,"home/signin.html",context={})

def dashboard(request):
    return render(request,"home/dashboard.html",context={})