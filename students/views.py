from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from accommodation.models import Booking, Room, Apartment, Block
from accommodation.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from accommodation.models import Booking, Complaint
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accommodation.models import MaintenanceRequest
from django.utils import timezone
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone

from django.shortcuts import render, redirect
from django.contrib import messages
from accommodation.models import Room, Booking
from django.contrib.auth.decorators import login_required

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from accommodation.models import Room, Booking,Accommodation
from django.core.paginator import Paginator




def dashbordDeluxe(request):
    return render(request, 'user/dashbordDeluxe.html')




def dashbordpremium(request):
    return render(request, 'user/dashbordpremium.html')


@login_required
def studentdashboard(request):
    user = request.user 

    current_booking = Booking.objects.filter(
        student=user,
        status='active'
    ).select_related('room__apartment__block').first()

    return render(request, 'user/studentdashboard.html', {
        'user': user,
        'current_booking': current_booking
    })


from django.shortcuts import render


from django.shortcuts import render
import pycountry

def get_country_code(name):
    try:
        country = pycountry.countries.get(name=name)
        if country:
            return country.alpha_2.lower()
    except:
        return None


def apply_room(request):
    rooms = Room.objects.select_related('apartment', 'apartment__block').filter(
    status__in=['available', 'occupied'],                   
    apartment__status='Active'           
)

    

    deluxe_rooms = []
    premium_rooms = []
    all_rooms = []
    all_blocks = Block.objects.all() 
    all_accommodations = Accommodation.objects.values('name').distinct()


    for room in rooms:
        # Find the active booking for this room (if any)
        active_booking = Booking.objects.filter(room=room, status='active').select_related('student').first()
        residents = []

        resident_info = None
        if active_booking:
            student = active_booking.student
            country_name = student.country if student.country else None
            country_code = get_country_code(country_name)
            resident_info = {
                'country': student.country if student.country else None,
                'flag':country_code,
                'course': student.program,
            }
            residents.append({
                'country': student.country,
                'flag': get_country_code(student.country),
                'course': student.program
                
            })
        all_rooms.append({
            'id': room.room_number,
            'name': room.room_number,
            'block': room.apartment.block.name,
            'type': room.apartment.type,
            'residents': residents,
            'accommodation': room.apartment.block.accommodation.name,
            'level': room.apartment.level
        })    

        room_data = {
            'name': room.room_number,
            'block': room.apartment.block.name,
            'type': room.apartment.type,
            'resident': resident_info,
            'accommodation': room.apartment.block.accommodation.name,
        }

        if room.apartment.type.lower() == 'deluxe':
            deluxe_rooms.append(room_data)
        elif room.apartment.type.lower() == 'premium':
            premium_rooms.append(room_data)



    context = {
        'all_blocks': all_blocks,
        'all_accommodations': all_accommodations,
        'all_rooms_json': json.dumps(all_rooms, cls=DjangoJSONEncoder),
        'deluxe_rooms': deluxe_rooms,
        'premium_rooms': premium_rooms
    }
    

    return render(request, 'user/apply_room.html', context)
from django.shortcuts import render


from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def reapplying(request):
    try:
        booking = Booking.objects.select_related("room__apartment__block").filter(
            student=request.user,
            status='active'
        ).latest('booking_date')
        room = booking.room
    except Booking.DoesNotExist:
        messages.error(request, "No active booking found. You must have an existing booking to reapply.")
        room = None
        booking = None  

    return render(request, 'user/Reapplying.html', {
        'room': room,
        'booking':booking
    })
from datetime import datetime, timedelta
from django.utils.timezone import now, make_aware
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.timezone import localtime


@login_required
def reapply_action(request):
    try:
        booking = Booking.objects.select_related("room__apartment__block").filter(
            student=request.user,
            status='active'
        ).latest('booking_date')

        today = now().date()
       

        expire_date = localtime(booking.expiration_date).date()  # Convert UTC → Malaysia time


        # ✅ Only allow if within 30 days of expiration
        if (expire_date - today).days > 30:
            messages.warning(request, f"You can only reapply within 30 days of expiration. Your current expiration is {expire_date}.")
            return redirect('reapplying')

        # 🔁 Calculate next expiration
        year = expire_date.year
        if expire_date.month == 5:
            next_expiration = datetime(year, 9, 1)
        elif expire_date.month ==9:
            next_expiration = datetime(year + 1, 2, 1)
        elif expire_date.month == 2:
            next_expiration = datetime(year, 5, 31)
        else:
            messages.warning(request, "Your expiration date doesn't match any standard semester.")
            return redirect('reapplying')

        booking.expiration_date = make_aware(next_expiration)
        booking.save()

        messages.success(request, f"Reapplied successfully. New expiration date: {booking.expiration_date.date()}")
        return redirect('user_profile')

    except Booking.DoesNotExist:
        messages.error(request, "No active booking found.")
        return redirect('user_profile')





def reapplying_confirmation(request):
    return render(request, 'user/reapplying_confirmation.html')

@login_required
def confirmation(request):

  
    return render(request, 'user/confirmation.html')



@login_required
def final_confirmation(request):
    room_id = request.GET.get('room_id')
    if not room_id:
        messages.error(request, "No room ID provided.")
        return redirect('apply_room')

    room = get_object_or_404(Room, room_number=room_id)

    if room.status=="occupied":
        messages.error(request, "This room is already occupied.")
        return redirect('apply_room')

    # Check if student has already booked
    if Booking.objects.filter(student=request.user,status="active").exists():
        messages.warning(request, "You have already booked a room.")
        return redirect('studentdashboard')

    # Create booking
    Booking.objects.create(
        student=request.user,
        booking_date=timezone.now().date(),
        room=room,
        status="active"
    )

    # Update room status
    room.status = "occupied"
    room.save()

    messages.success(request, f"You have successfully booked Room {room.room_number}!")
    return redirect('studentdashboard')  


@login_required
def maintenance(request):
    if request.method == 'POST':
        issue_type = request.POST.get('issue_type')
        description = request.POST.get('description')

        try:
            booking = Booking.objects.get(student=request.user, status='active')
            room = booking.room
        except Booking.DoesNotExist:
            messages.error(request, "You must have an active booking to submit a maintenance request.")
            return redirect('student_maintenance')

        MaintenanceRequest.objects.create(
            room=room,
            issue_type=issue_type,
            description=description
        )

        messages.success(request, "Maintenance request submitted successfully.")
        return redirect('student_maintenance')

    # Retrieve all maintenance requests by this user, even if the room is inactive now
    maintenance_requests = MaintenanceRequest.objects.filter(
        room__booking__student=request.user
    ).distinct().order_by('-date_reported')

    return render(request, 'user/student_maintenance.html', {
        'maintenance_requests': maintenance_requests
    })


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def cancel_booking(request):
    student = request.user  # Assumes the user is a student

    # Get the active booking
    booking = Booking.objects.filter(student=student, status='active').select_related('room').first()

    if not booking:
        messages.warning(request, "You do not have any active bookings.")
        return redirect('studentdashboard')

    if request.method == 'POST':
        # Cancel the booking
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f"Booking for Room {booking.room.room_number} has been cancelled.")
        return redirect('user_profile')

    # Room price logic
    room_type = booking.room.apartment.type.lower()
    if room_type == "premium":
        price = 575
    elif room_type == "deluxe":
        price = 420
    else:
        price = 0

    context = {
        'booking': booking,
        'price': price
    }
    return render(request, 'user/Cancellation_Booking_Page.html', context)

  # Rename the file to use underscore if possible

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required
def complain(request):
    if request.method == 'POST':
        subject = request.POST.get('subject')
        description = request.POST.get('description')

        if subject and description:
            Complaint.objects.create(
                student=request.user,
                subject=subject,
                description=description
            )
            messages.success(request, "Complaint submitted successfully.")
            return redirect('complain')
        else:
            messages.error(request, "Both subject and description are required.")

    complaints = Complaint.objects.filter(student=request.user).order_by('-date')

    return render(request, 'user/complain.html', {
        'complaints': complaints
    })


