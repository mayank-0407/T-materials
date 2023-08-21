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

def redirect_admin(request):
    url="http://127.0.0.1:8000/admin"
    response=redirect(url)
    return response

def request_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('home')

def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('redirect_admin')
        return redirect('dashboard') 

    if request.method == 'POST':
        temp_email=request.POST.get('email')
        password=request.POST.get('pass1')
        
        email=temp_email.lower()
            
        try:
            verify_user=User.objects.get(email=email)    
        except:
            messages.error(request, 'Entered Email is ot registered !')
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
    try:
        temp_user=User.objects.get(username=request.user.username)
        main_user=Main_user.objects.get(user=temp_user)
    except:
        print('Not able t find data in home')
    if main_user.is_cr:
        return gr_dashboard(request)
    return main_dashboard(request)

def main_dashboard(request):
    try:
        temp_user=User.objects.get(username=request.user.username)
        main_user=Main_user.objects.get(user=temp_user)
    except:
        print('Not able t find data in home')
    all_slides=Slides.objects.filter(my_session=main_user.my_session).all()
    print(all_slides)
    return render(request,"home/dashboard.html",context={'all_slides':all_slides})

def gr_dashboard(request):
    try:
        temp_user=User.objects.get(username=request.user.username)
        main_user=Main_user.objects.get(user=temp_user)
    except:
        print('Not able t find data in home')
    all_slides=Slides.objects.filter(my_session=main_user.my_session).all()
    print(all_slides)
    return render(request,"home/gr/gr_dashboard.html",context={'all_slides':all_slides})

def add_subject(request):
    if request.method=='POST':
        subject_name=request.POST.get('sub_name')
        drive_link=request.POST.get('sub_link')
        sub_code=request.POST.get('sub_code')

        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
        except:
            print('Not able t find data in subject')
        try:
            main_session=Session.objects.get(group=main_user.my_session)
            print(main_user.my_session)
        except:
            print('Error while creating slide')
        my_slide=Slides.objects.create(my_session=main_user.my_session,sub_name=subject_name,code=sub_code,link=drive_link)
        my_slide.save()

        messages.error(request, 'Subject Added Successfully')
        return redirect('dashboard')
    
def new_notification(request):
    if request.method=='POST':
        notification_detail=request.POST.get('noti_details')

    try:
        temp_user=User.objects.get(username=request.user.username)
        main_user=Main_user.objects.get(user=temp_user)
    except:
        print('Not able t find data in notification')

    try:
        my_slide=Notification.objects.create(my_session=main_user.my_session,information=notification_detail)
        my_slide.save()
    except:
        print('Error while adding new slide')
    messages.error(request, 'New Notification Sent Successfully')
    return redirect('dashboard')