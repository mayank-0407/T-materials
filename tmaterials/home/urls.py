from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('admin/',views.redirect_admin,name="redirect_admin"),
    path('temp/',views.temp,name="view_temp"),
    path('',views.home,name="home"),
    path('logout/',views.request_logout,name="request_logout"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('dashboard/view/students/',views.view_all_students,name="view_all_students"),
    path('dashboard/add/students/',views.add_student,name="add_student"),
    path('dashboard/upload/students/',views.student_upload,name="student_upload"),
    path('dashboard/sub/del/<int:id>/',views.del_sub_session,name="del_sub_session"),
    path('dashboard/addsubject/',views.add_subject,name="add_subject"),
    path('dashboard/new/notification/',views.new_notification,name="new_noti"),
    path('dashboard/view/notifications/',views.view_all_notifications,name="view_all_notifications"),
    path('dashboard/view/notifications/del/<int:id>/',views.del_noti,name="del_noti"),
    path('dashboard/add/deadline/',views.add_deadline,name="add_deadline"),
    path('dashboard/view/deadlines/',views.view_all_deadlines,name="view_all_deadlines"),
    path('dashboard/view/deadlines/del/<int:id>/',views.del_deadline,name="del_deadline"),
    path('dashboard/add/eval/',views.add_evaluation,name="add_evaluation"),
    path('dashboard/view/eval/',views.view_all_evaluations,name="view_all_evaluations"),
    path('dashboard/view/eval/del/<int:id>/', views.del_eval, name='del_eval'),
    path('dashboard/view/eval/edit/<int:id>/',views.edit_evaluations,name="edit_evaluations"),
    path('dashboard/view/eval/edit/update/',views.update_edit_evaluations,name="update_edit_evaluations"),
]