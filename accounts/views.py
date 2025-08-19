from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
# views.py
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from accommodation.models import Booking, Room, Apartment, Block




def student_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email, role='student')
        except User.DoesNotExist:
            messages.error(request, "No student account found with this email.")
            return render(request, 'general/studentlogin.html')

        user = authenticate(request, user_id=user.user_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('studentdashboard')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'general/studentlogin.html')

def admin_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email, role='admin')
        except User.DoesNotExist:
            messages.error(request, "No admin account found with this email.")
            return render(request, 'general/adminlogin.html')

        user = authenticate(request, user_id=user.user_id, password=password)
        if user is not None:
            login(request, user)
            return redirect('admindashboard')
        else:
            messages.error(request, "Invalid credentials.")

    return render(request, 'general/adminlogin.html')

@login_required
def adminprofile(request):
    user = request.user 
  

    if request.method == 'POST':
        if request.user.email == "ad14725836@uniten.com":
                messages.error(request, "Demo mode: You cannot change profile data.")
                return redirect('adminprofile')
        phone = request.POST.get('phone_number', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        user.phone_number = phone
        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)
        user.save()
       

        messages.success(request, "Profile updated successfully.")
        return redirect('adminprofile')

    return render(request, 'my_admin_website/AdminProfile.html', {'user': user})

@login_required
def user_profile(request):
    
    user = request.user
    current_booking = Booking.objects.filter(student=user, status='active').select_related('room__apartment__block').first()
    current_room = current_booking.room if current_booking else None

    if request.method == 'POST':
        if request.user.email == "CS30584216@uniten.edu":
                messages.error(request, "Demo mode: You cannot change profile data.")
                return redirect('user_profile')
        phone = request.POST.get('phone_number', '').strip()
        new_password = request.POST.get('new_password', '').strip()

        user.phone_number = phone
        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user)

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('user_profile')
    

    return render(request, 'user/user_profile.html', {'user': user, 'current_room': current_room})



