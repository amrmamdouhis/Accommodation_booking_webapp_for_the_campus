from django.urls import path
from . import views

urlpatterns = [
     # User pages
    path('studentdashboard/', views.studentdashboard, name='studentdashboard'),
    path('apply_room/', views.apply_room, name='apply_room'),
    path('reapplying/', views.reapplying, name='reapplying'),
    path('reapplying_confirmation/', views.reapplying_confirmation, name='reapplying_confirmation'),
    path('complain/', views.complain, name='complain'),
    path('apply_room/confirmation/', views.confirmation, name='confirmation'),
    path('student_maintenance/', views.maintenance, name='student_maintenance'),
    path('Cancellation_Booking_Page/', views.cancel_booking, name='cancellation'),
    path('apply_room/confirm/room/', views.final_confirmation, name='final_confirmation'),
    path('students/reapply_action/', views.reapply_action, name='reapply_action'),



    path('dashbordDeluxe/', views.dashbordDeluxe, name='dashbordDeluxe'),
    path("dashbordpremium/", views.dashbordpremium, name="dashbordpremium"),
   
]