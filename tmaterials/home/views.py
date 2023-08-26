from django.shortcuts import render, HttpResponse,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime, timedelta
import pandas as pd

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
            messages.error(request, 'Entered Email is not registered !')
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
    if request.user.is_authenticated:
        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
        except:
            print('Not able t find data in home')
        if main_user.is_cr:
            return gr_dashboard(request)
        return main_dashboard(request)
    return redirect('home')

def main_dashboard(request):
    if request.user.is_authenticated:
        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
        except:
            print('Not able t find data in home')
        all_slides=Slides.objects.filter(my_session=main_user.my_session).all()
        
        all_notifications=Notification.objects.filter(my_session=main_user.my_session).all()
        all_notifications_count=Notification.objects.filter(my_session=main_user.my_session).all().count()
        return render(request,"home/dashboard.html",context={'all_slides':all_slides,'all_notifications':all_notifications,'all_notifications_count':all_notifications_count})
    return redirect('home')
    
def gr_dashboard(request):
    if request.user.is_authenticated:
        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
        except:
            print('Not able t find data in home')
        all_slides=Slides.objects.filter(my_session=main_user.my_session).all()
        all_subj=Slides.objects.filter(my_session=main_user.my_session).all()
        all_notifications=Notification.objects.filter(my_session=main_user.my_session).all()
        all_notifications_count=Notification.objects.filter(my_session=main_user.my_session).all().count()
        return render(request,"home/gr/gr_dashboard.html",context={'all_slides':all_slides,'all_subj':all_subj,'all_notifications':all_notifications,'all_notifications_count':all_notifications_count})
    return redirect('home')

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

def view_all_notifications(request):
    if request.user.is_authenticated:
        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
        except:
            print('Not able t find data in home')
        
        all_notifications=Notification.objects.filter(my_session=main_user.my_session).all()
        all_notifications_count=Notification.objects.filter(my_session=main_user.my_session).all().count()
        # all_notifications.reverse()
        return render(request,"home/announcements.html",context={'all_notifications':all_notifications,'all_notifications_count':all_notifications_count,'main_user':main_user})
    return redirect('home')

def add_deadline(request):
    if request.method=='POST':
        sub_name=request.POST.get('sub_name')
        # sub_code=request.POST.get('sub_code')
        deadline_info=request.POST.get('deadline_info')

        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
            my_sub_slide=Slides.objects.get(pk=sub_name)
        except:
            print('Not able t find data in notification')

        try:
            my_deadline=Deadline.objects.create(my_session=main_user.my_session,my_slide=my_sub_slide,
                                                sub_name=my_sub_slide.sub_name,code=my_sub_slide.code,
                                                information=deadline_info)
            my_deadline.save()
            notification_detail='New Deadline Added !!'
            deadline_notification=Notification.objects.create(my_session=main_user.my_session,information=notification_detail)
            deadline_notification.save()
        except:
            print('Error while adding new slide')
        messages.error(request, 'New Notification Sent Successfully')
        return redirect('dashboard')

def view_all_deadlines(request):
    if request.user.is_authenticated:
        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
        except:
            print('Not able t find data in home')
        
        all_deadlline=Deadline.objects.filter(my_session=main_user.my_session).all()
        all_subj=Slides.objects.filter(my_session=main_user.my_session).all()
        all_notifications=Notification.objects.filter(my_session=main_user.my_session).all()
        all_notifications_count=Notification.objects.filter(my_session=main_user.my_session).all().count()

        return render(request,"home/all_deadlines.html",context={'main_user':main_user,'all_deadline':all_deadlline,'all_subj':all_subj,'all_notifications':all_notifications,'all_notifications_count':all_notifications_count})
    return redirect('home')

def add_evaluation(request):
    if request.method=='POST':
        sub_name=request.POST.get('sub_name')
        # sub_code=request.POST.get('sub_code')
        eval_type=request.POST.get('eval_type')
        eval_room=request.POST.get('eval_room')
        end_date=str(request.POST.get('end_date'))
        eval_information=request.POST.get('eval_information')

        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
            my_sub_slide=Slides.objects.get(pk=sub_name)
        except:
            print('Not able t find data in notification')

        now = datetime.now()
        time=now.time()

        try:
            my_evaluation=Evaluation.objects.create(my_session=main_user.my_session,sub_name=my_sub_slide.sub_name,code=my_sub_slide.code,
                                                    my_slide=my_sub_slide,eval_type=eval_type,
                                                    eval_room=eval_room,eval_information=eval_information)
            my_evaluation.save()
            notification_detail='New Subject Evaluation Announced!!'
            deadline_notification=Notification.objects.create(my_session=main_user.my_session,information=notification_detail)
            deadline_notification.save()
        except:
            print('Error while adding new eval')
        messages.error(request, 'New Evaluation added Successfully')
        return redirect('dashboard')

def view_all_evaluations(request):
    if request.user.is_authenticated:
        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
            my_subj=Slides.objects.filter(my_session=main_user.my_session).all()
        except:
            print('Not able t find data in home')
        
        all_evaluations=Evaluation.objects.filter(my_session=main_user.my_session).all()
        all_notifications=Notification.objects.filter(my_session=main_user.my_session).all()
        all_notifications_count=Notification.objects.filter(my_session=main_user.my_session).all().count()
        return render(request,"home/all_evaluations.html",context={'main_user':main_user,'all_evaluations':all_evaluations,'all_notifications':all_notifications,'all_notifications_count':all_notifications_count})
    return redirect('home')

def edit_evaluations(request,id):
    if request.user.is_authenticated:
        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
            this_evaluations=Evaluation.objects.get(pk=id)
        except:
            print('Not able t find data in edit eval')
        
        all_notifications=Notification.objects.filter(my_session=main_user.my_session).all()
        all_notifications_count=Notification.objects.filter(my_session=main_user.my_session).all().count()
        return render(request,"home/edit_evaluations.html",context={'this_evaluations':this_evaluations,'all_notifications':all_notifications,'all_notifications_count':all_notifications_count})
    return redirect('home')

def update_edit_evaluations(request):
    if request.method == 'POST':
        sub_id=request.POST.get('sub_id')
        sub_name=request.POST.get('sub_name')
        eval_type=request.POST.get('eval_type')
        eval_room=request.POST.get('eval_room')
        eval_information=request.POST.get('eval_information')
        print(eval_information)
        try:
            my_evaluation=Evaluation.objects.get(pk=sub_id)
            my_evaluation.sub_name=sub_name
            my_evaluation.eval_type=eval_type
            my_evaluation.eval_room=eval_room
            my_evaluation.eval_information=eval_information
            my_evaluation.save()
        except:
            messages.error(request, 'Internal Server Error - Unable to Find Evaluation !')
            return redirect('view_all_evaluations')

        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
        except:
            print('Not able t find update edit eval in home')

        notification_detail='Updated Announced Subject ( '+ str(sub_name) +' ) Evaluation!!'
        deadline_notification=Notification.objects.create(my_session=main_user.my_session,information=notification_detail)
        deadline_notification.save()
        messages.error(request, 'Updated Evaluation Details !')
        return redirect('view_all_evaluations')
    messages.error(request, 'Updatedion of Evaluation Details Unsuccessful !')
    return redirect('view_all_evaluations')

def del_eval(request,id):
    if request.method == 'POST':
        try:
            this_evaluations=Evaluation.objects.get(pk=id)
            this_evaluations.delete()
            messages.error(request, 'Evaluation Details has been deleted Successfully')
            return redirect('view_all_evaluations')
        except:
            messages.error(request, 'Error while deleting Evaluation Details.')
            return redirect('dashboard')
    
def del_deadline(request,id):
    if request.method == 'POST':
        try:
            this_deadl=Deadline.objects.get(pk=id)
            this_deadl.delete()
            messages.error(request, 'Deadline Details has been deleted Successfully')
            return redirect('view_all_deadlines')
        except:
            messages.error(request, 'Error while deleting Deadline Details.')
            return redirect('dashboard')

def del_noti(request,id):
    if request.method == 'POST':
        try:
            this_noti=Notification.objects.get(pk=id)
            this_noti.delete()
            messages.error(request, 'Notification Details has been deleted Successfully')
            return redirect('view_all_notifications')
        except:
            messages.error(request, 'Error while deleting Notification Details.')
            return redirect('dashboard')
    
def del_sub_session(request,id):
    if request.method == 'POST':
        try:
            this_slide=Slides.objects.get(pk=id)
            this_slide.delete()
            messages.error(request, 'The Subject Details has been deleted Successfully')
            return redirect('dashboard')
        except:
            messages.error(request, 'Error while deleting Subject Details.')
            return redirect('dashboard')
        
def view_all_students(request):
    if request.user.is_authenticated:
        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
        except:
            print('Not able t find data in home')
        
        all_notifications=Notification.objects.filter(my_session=main_user.my_session).all()
        all_notifications_count=Notification.objects.filter(my_session=main_user.my_session).all().count()

        all_students=Main_user.objects.filter(my_session=main_user.my_session).all()
        return render(request,"home/all_students.html",context={'all_students':all_students,'main_user':main_user,'all_notifications':all_notifications,'all_notifications_count':all_notifications_count})
    return redirect('home')

def add_student(request):
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        Last_name=request.POST.get('Last_name')
        stu_roll=request.POST.get('stu_roll')
        temp_email=request.POST.get('email')
        pass1=request.POST.get('pass1')
        
        email=temp_email.lower()
            
        try:
            verify_user=User.objects.get(email=email)    
            if verify_user:
                messages.error(request, 'Entered Email is already registered !')
                return redirect('dashboard')
        except:
            pass
        myuser=User.objects.create_user(username=email,email=email,first_name=first_name,last_name=Last_name)
        myuser.set_password(pass1)
        myuser.save()
        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
        except:
            print('Not able t find data in Add Student dashboard')
        try:
            Main_user.objects.create(user=myuser, roll_no=stu_roll,
                                my_session=main_user.my_session)
        except Exception as e:
            User.objects.get(id=myuser.id).delete()
            return HttpResponse(str(e))
        messages.error(request, 'Student Added Successfully.')
        return redirect('view_all_students')
    
def student_upload(request):
    if request.user.is_superuser:
        logout(request)
        messages.error(request, 'Error - Super user Dont have Access.')
        return redirect('home')
    if request.user.is_authenticated:
        if request.method=="POST":
            try:
                file=request.FILES.get('file')
                try:
                    if str(file).endswith('.csv'):
                        rfile=pd.read_csv(file)
                    elif str(file).endswith('.xlsx'):
                        rfile=pd.read_excel(file)
                    else:
                        messages.error(request, 'Error - File Format not valid')
                        return redirect('dashboard')
                    
                    return student_uploader(request,rfile)
                    
                except:
                    messages.error(request, 'Error - File not valid')
                    return redirect('dashboard')
            except:
                messages.error(request, 'Error - cant read the file')
                return redirect('dashboard')
        
    else:    
        return redirect("signin")
    
def student_uploader(request,rfile):
    # mycompany=Company.objects.get(user=request.user)

    if 'Email' not in rfile.columns:
        messages.error(request, 'Please add an "Email" column in your file and try uploading again!!')
        return redirect('dashboard')
    
    invalid_email=[]
    Error_while_generating_student=[]
    Error_while_generating_student_flag=False
    invalid_email_flag=False
    
    for i in range(len(rfile['Email'])):
        
        email = rfile["Email"][i]
        fname = rfile["FirstName"][i]
        lname = rfile["LastName"][i]
        rollno = rfile["RollNo"][i]
        
        try:
            User.objects.get(email=email)
            invalid_email.append(email)
            invalid_email_flag=True
            continue
        except:
            pass
        
        email.lower()
        newuser=User.objects.create_user(first_name=fname,last_name=lname,
                                        email=email, username=email)
        try:
            temp_user=User.objects.get(username=request.user.username)
            main_user=Main_user.objects.get(user=temp_user)
        except:
            print('Not able t find data in Add Student dashboard')
        pass1 = 'qwerty@'+str(main_user.my_session)
        newuser.set_password(pass1)
        newuser.save()
        
        try:
            Main_user.objects.create(user=newuser,my_session=main_user.my_session,roll_no=rollno)
        except Exception as e:
            User.objects.get(id=newuser.id).delete()
            Error_while_generating_student.append(i+1)
            Error_while_generating_student_flag=True
        
        # try:
        #     email_message='Account Creation By GR'
        #     email_subject='Your Account at T-materials has been created successfully.'+'Email : '+ email + 'Temporary Password : ' + pass1
        #     SENDMAIL(email_message,email_subject,email)
        # except:
        #     continue
    if invalid_email_flag ==True and Error_while_generating_student_flag==True:
        messages.error(request,'Accounts Already exisits for these emails:-'+str(invalid_email)+'System was not able to create account for these Students :-'+str(Error_while_generating_student))
        return redirect('dashboard')
    elif invalid_email_flag==True:
        messages.error(request, 'Accounts Already exisits for these emails:-'+str(invalid_email))
        return redirect('dashboard')
    elif Error_while_generating_student_flag==True:
        messages.error(request,'System was not able to create account for these Students :-'+str(Error_while_generating_student))
        return redirect('dashboard')
    else:
        messages.error(request, 'Success - Students Added Successfully')
        return redirect('dashboard')