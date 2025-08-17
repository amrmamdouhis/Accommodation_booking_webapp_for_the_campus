from django.urls import path, include
from django.contrib import admin
from . import views


urlpatterns = [
    path('studentlogin/', views.student_login, name='studentlogin'),
    path('adminlogin/', views.admin_login, name='admin-login'),
    path('my_admin_website/profile/', views.adminprofile, name='adminprofile'),
    path('user_profile/', views.user_profile, name='user_profile'),

]


