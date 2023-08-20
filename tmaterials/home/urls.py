from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('temp/',views.temp,name="view_temp"),
    path('',views.home,name="home"),
    path('dashboard/',views.dashboard,name="dashboard"),
]