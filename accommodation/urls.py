from django.urls import path
from . import views

urlpatterns = [
    # General/User Pages
    path('', views.homepage, name='homepage'),
    path('premium/', views.premium, name='premium'),
    path('deluxe/', views.deluxe, name='deluxe'),
    path('faq/', views.faq, name='faq'),
    path('guidelines/', views.guidelines, name='guidelines'),
    path('facilities/', views.facilities, name='facilities'),

    # Admin Pages
    path('my_admin_website/dashboard/', views.admindashboard, name='admindashboard'),
    path('my_admin_website/bookings/', views.adminbookings, name='adminbookings'),
    path('my_admin_website/complaints/', views.admincomplaints, name='admincomplaints'),
    path('my_admin_website/apartments/', views.manage_apartments, name='adminapartments'),
    path('my_admin_website/Adminaddstudents/', views.Adminaddstudents, name='Adminaddstudents'),
    path('my_admin_website/edit-apartment/<int:apartment_id>/', views.edit_apartment, name='edit_apartment'),
    path('toggle-apartment-status/<int:apartment_id>/', views.toggle_apartment_status, name='toggle_apartment_status'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('my_admin_website/maintenance/', views.adminmaintenance, name='maintenance'),
    path('get-blocks/<int:accommodation_id>/', views.get_blocks, name='get_blocks'),
    path('get-apartments/<int:block_id>/', views.get_apartments, name='get_apartments'),
    path('get-rooms/<int:apartment_id>/', views.get_rooms, name='get_rooms'),





    # path('add-accommodation/', views.add_accommodation, name='add_accommodation'),

    
   
    
]

