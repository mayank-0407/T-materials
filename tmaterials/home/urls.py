from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('admin/',views.redirect_admin,name="redirect_admin"),
    path('temp/',views.temp,name="view_temp"),
    path('',views.home,name="home"),
    path('logout/',views.request_logout,name="request_logout"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('dashboard/addsubject',views.add_subject,name="add_subject"),
    path('dashboard/newnotification',views.new_notification,name="new_noti"),
    path('dashboard/viewnotifications',views.view_all_notifications,name="view_all_notifications"),
]