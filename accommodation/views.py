import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AddStudentForm,AccommodationForm,ApartmentForm,ApartmentEditForm,Booking
from accounts.models import User
from .models import Accommodation
from .models import Apartment, Block
from django.db.models import Q ,Count
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import get_object_or_404
from .forms import BookingForm
from django.http import JsonResponse
from .models import Block, Apartment, Room
from django.utils import timezone
from .models import Complaint
from .forms import ComplaintReplyForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from accommodation.models import Room  
from django.shortcuts import render, redirect
from .models import Room, MaintenanceRequest
def homepage(request):
    return render(request, 'general/homepage.html')

def faq(request):
    return render(request, 'general/faq.html')

def guidelines(request):
    return render(request, 'general/guidelines.html')

def student_login(request):
    return render(request, 'general/studentlogin.html')

def admin_login(request):
    return render(request, 'general/adminlogin.html')

def premium(request):
    return render(request, 'general/premium.html')

def deluxe(request):
    return render(request, 'general/deluxe.html')
def facilities(request):
    return render(request, 'general/facilities.html')

def adminapartments(request):
    return render(request, 'my_admin_website/AdminApartments.html')

def admindashboard(request):
    user = request.user 
    return render(request, 'my_admin_website/AdminDashboard.html',{'user': user})


def get_blocks(request, accommodation_id):
    blocks = Block.objects.filter(accommodation_id=accommodation_id).values('id', 'name')
    return JsonResponse(list(blocks), safe=False)

def get_apartments(request, block_id):
    apt_type = request.GET.get('type')
    if apt_type:
        print(apt_type)
        apartments = Apartment.objects.filter(block_id=block_id, type=apt_type)
    else:
        apartments = Apartment.objects.filter(block_id=block_id)
    
    data = [{'id': apt.id, 'apartment_number': apt.apartment_number} for apt in apartments]
    return JsonResponse(data, safe=False)

def get_rooms(request, apartment_id):
    rooms = Room.objects.filter(
        apartment_id=apartment_id,
        status='available'  # Only include available rooms
    ).values('apartment_id', 'room_number')
    
    return JsonResponse(list(rooms), safe=False)


def Adminaddstudents(request):
    form = AddStudentForm()
    if request.method == 'POST':
        if 'add_student' in request.POST:
            form = AddStudentForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Student added successfully.')
                return redirect('Adminaddstudents')  

            else:
            
                messages.error(request, 'Error adding student.')
                return redirect('Adminaddstudents')  


        elif 'upload_excel' in request.POST and request.FILES.get('excel_file'):
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file)
                for _, row in df.iterrows():
                    user_id = str(row['student_id']).strip()
                    email = f"{user_id}@uniten.edu"

                    if not User.objects.filter(user_id=user_id).exists():
                        User.objects.create_user(
                            user_id=user_id,
                            name=row['name'],
                            email=email,
                            program=row['program'],
                            country=row['country'],
                            password=f"uni10pass!",
                            role='student'
                        )
                messages.success(request, "Students imported successfully.")
            except Exception as e:
                messages.error(request, f"Error processing file: {e}")

    else:
        form = AddStudentForm()

    return render(request, 'my_admin_website/Adminaddstudents.html',{'form':form})

def manage_apartments(request):
    apartment_form = ApartmentForm()
    accommodation_form = AccommodationForm()
    blocks = Block.objects.all()
    apartments = Apartment.objects.select_related('block', 'block__accommodation').annotate(
    available_rooms_count=Count('room', filter=Q(room__status='available'))).order_by('-available_rooms_count')
    
    apartment_forms = {apt.id: ApartmentEditForm(instance=apt) for apt in apartments}

    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status')

    if query:
        apartments = apartments.filter(
            Q(block__name__icontains=query) | Q(apartment_number__icontains=query)
        )

    if status_filter:
        apartments = apartments.filter(status=status_filter)

    if request.method == 'POST':
        # Add apartment via form
        if 'add_apartment' in request.POST:
            apartment_form = ApartmentForm(request.POST)
            if apartment_form.is_valid():
                apartment = apartment_form.save()
               
                for i in range(1, 5):
                    Room.objects.create(
                        apartment=apartment,
                        room_number=f"{apartment.apartment_number}-R{i}",
                        status='available'
                       
                    )
                messages.success(request, "Apartment and 4 rooms created successfully.")
                messages.success(request, "Apartment added successfully.")
                return redirect('adminapartments')  

            else:
                messages.error(request, "Failed to add apartment.")
                return redirect('adminapartments')  


       # Add accommodation via form
        elif 'add_accommodation' in request.POST:
            accommodation_form = AccommodationForm(request.POST)
            if accommodation_form.is_valid():
                accommodation = accommodation_form.save()

                try:
                    num_blocks = int(request.POST.get('number_of_blocks', 0))
                except ValueError:
                    num_blocks = 0

                for i in range(1, num_blocks + 1):
                    block_name = request.POST.get(f'block_name_{i}')
                    if block_name:
                        Block.objects.create(name=block_name, accommodation=accommodation)

                messages.success(request, "Accommodation and blocks added successfully.")
                return redirect('adminapartments') 
            else:
                messages.error(request, "Failed to add accommodation.")
                return redirect('adminapartments') 

        
        # Upload Excel for apartments
        elif 'upload_excel' in request.POST and request.FILES.get('excel_file'):
            
            excel_file = request.FILES['excel_file']
            try:
                df = pd.read_excel(excel_file, engine='openpyxl')
                valid_types = dict(Apartment.ROOM_TYPES).keys()
                
            

                for _, row in df.iterrows():
                    accommodation_name = str(row['accommodation']).strip()
                    block_name = str(row['block']).strip()

                    # Lookup Accommodation
                    try:
                        accommodation = Accommodation.objects.get(name__iexact=accommodation_name)
                    except Accommodation.DoesNotExist:
                        messages.error(request, f"Accommodation '{accommodation_name}' does not exist.")
                     

                        continue

                    # Lookup Block under that accommodation
                    try:
                        block = Block.objects.get(accommodation=accommodation, name__iexact=block_name)
                        print(block)
                    except Block.DoesNotExist:
                        messages.error(request, f"Block '{block_name}' not found under '{accommodation_name}'.")
                        

                        continue
                    apt_type = str(row['apartment_type']).strip()
                    if apt_type not in valid_types:
                       messages.error(request, f"Invalid apartment type '{apt_type}' for apartment '{row['apartment_number']}'.")
                       continue
                       


                    # Create Apartment
                
                    apartment =Apartment.objects.create(
                        block=block,
                        apartment_number=row['apartment_number'],
                        level=int(row['level']),
                        status='Active',
                        type=apt_type
                    )
                    for i in range(1, 5):
                     Room.objects.create(
                        apartment=apartment,
                        room_number=f"{apartment.apartment_number}-R{i}",
                        status='available'
                        
                       
                    )
                      
                messages.success(request, " 4 rooms for each Apartments created successfully.")

                messages.success(request, "Apartments uploaded successfully.")
                return redirect('adminapartments') 
            except Exception as e:
                messages.error(request, f"Upload failed: {e}")
                return redirect('adminapartments') 
                # PAGINATE
    paginator = Paginator(apartments, 5)  
    page = request.GET.get('page')
    try:
        apartments = paginator.page(page)
    except PageNotAnInteger:
        apartments = paginator.page(1)
    except EmptyPage:
        apartments = paginator.page(paginator.num_pages)

    context = {
        'apartment_form': apartment_form,
        'accommodation_form': accommodation_form,
        'apartments': apartments,  
        'apartment_forms': apartment_forms,
        'blocks': blocks,  
    }
    return render(request, 'my_admin_website/AdminApartments.html', context)




from django.db.models import Q
from .models import Apartment, Room, Booking  # adjust imports as needed

def edit_apartment(request, apartment_id):
    if request.method == 'POST':
        apartment = get_object_or_404(Apartment, id=apartment_id)

        old_apartment_number = apartment.apartment_number
        old_status = apartment.status  
        new_apartment_number = request.POST.get('apartment_number').strip()
        new_level = request.POST.get('level')
        new_status = request.POST.get('status')

        # Update apartment fields
        apartment.apartment_number = new_apartment_number
        apartment.level = new_level
        apartment.status = new_status
        apartment.save()

        # ✅ If apartment number changed, update related room numbers
        if old_apartment_number != new_apartment_number:
          
            related_rooms = Room.objects.filter(apartment=apartment)
            for room in related_rooms:
                old_room_suffix = room.room_number.split("-")[-1]  # e.g. "R1"
                new_room_number = f"{new_apartment_number}-{old_room_suffix}"
              
                
                
                # Update primary key (room_number)
                # Create new room instance manually, then delete the old one
                room_data = {
                    'apartment': room.apartment,
                    'status': room.status,
                }

                # Create a new Room with new primary key
                new_room = Room(
                    room_number=new_room_number,
                    **room_data
                )
                new_room.save()

                # Move any bookings to new room
                Booking.objects.filter(room=room).update(room=new_room)

                # Delete old room
                room.delete()

        # ✅ Update room statuses if apartment status changed
        related_rooms = Room.objects.filter(apartment=apartment)
        if old_status != new_status:
            if new_status.lower() == 'inactive':
                related_rooms.update(status='inactive')
                Booking.objects.filter(
                    room__in=related_rooms,
                    status='active'
                ).update(status='cancelled')
            elif new_status.lower() == 'active':
                related_rooms.update(status='available')

        messages.success(request, "Apartment updated successfully.")

    return redirect('adminapartments')



from django.utils.timezone import now
from accommodation.models import Room, Booking  


def toggle_apartment_status(request, apartment_id): 
    apartment = get_object_or_404(Apartment, id=apartment_id)

    if apartment.status == 'Active':
        apartment.status = 'Inactive'
        apartment.save()

        # Set all related rooms to inactive
        Room.objects.filter(apartment=apartment).update(status='inactive')

        # Cancel all active bookings related to these rooms
        Booking.objects.filter(room__apartment=apartment, status='active').update(
            status='cancelled',
            expiration_date=now()
        )

        messages.success(request, f"Apartment {apartment.apartment_number} deactivated. All bookings and rooms updated.")
    
    else:
        apartment.status = 'Active'
        apartment.save()

     
        Room.objects.filter(apartment=apartment, status='inactive').update(status='available')

        messages.success(request, f"Apartment {apartment.apartment_number} activated. Rooms reactivated.")

    return redirect('adminapartments')









def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'cancelled'
    booking.save()
    messages.success(request, "Booking cancelled successfully.")
    return redirect('adminbookings')

def adminbookings(request):
    booking_form = BookingForm()
    accommodations = Accommodation.objects.all()
    bookings_list = Booking.objects.select_related('student', 'room', 'room__apartment__block')

    # Filtering
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', '')

    if search_query:
        bookings_list = bookings_list.filter(
            Q(student__name__icontains=search_query) |
            Q(student__user_id__icontains=search_query) |
            Q(room__room_number__icontains=search_query)
        )
    if status_filter:
        bookings_list = bookings_list.filter(status=status_filter)

    if request.method == 'POST' and 'add_booking' in request.POST:
        booking_form = BookingForm(request.POST)
        room_number = request.POST.get('room_number') 
       
        selected_room = Room.objects.get(room_number=room_number)
       
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.room = selected_room
            booking.booking_date = timezone.now()
            selected_room.status = 'occupied'
            selected_room.save()
            booking.save()
            messages.success(request, "Booking created successfully.")
            return redirect('adminbookings')
        else:
            messages.error(request, "Booking form is not valid.")

    # Pagination
    paginator = Paginator(bookings_list.order_by('-booking_date'), 5)
    page_number = request.GET.get('page')
    bookings = paginator.get_page(page_number)

    return render(request, 'my_admin_website/AdminBooking.html', {
        'booking_form': booking_form,
        'accommodations': accommodations,
        'bookings': bookings,
    })

# def admincomplaints(request):
#     return render(request, 'my_admin_website/AdminComplain.html')

def admincomplaints(request):
    complaints = Complaint.objects.select_related('student').order_by('-date')

    # Filters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    if search_query:
        complaints = complaints.filter(
           Q(student__name__icontains=search_query) |
            Q(student__user_id__icontains=search_query) |
            Q(subject__icontains=search_query)
        )

    if status_filter:
        complaints = complaints.filter(status=status_filter.lower())

    if request.method == 'POST' and 'submit_reply' in request.POST:
        complaint_id = request.POST.get('complaint_id')
        complaint = get_object_or_404(Complaint, id=complaint_id)

        form = ComplaintReplyForm(request.POST, instance=complaint)
        if form.is_valid():
            reply = form.cleaned_data['reply']
            complaint.reply = reply
            complaint.status = 'resolved'
            complaint.save()
            messages.success(request, 'Reply submitted successfully.')
            return redirect('admincomplaints')
        else:
            messages.error(request, 'Reply cannot be empty.')
    paginator = Paginator(complaints, 5)  # 5 complaints per page
    page_number = request.GET.get('page')
    complaints = paginator.get_page(page_number)

    return render(request, 'my_admin_website/AdminComplain.html', {
        'complaints': complaints,
    })


def adminmaintenance(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    maintenances = MaintenanceRequest.objects.select_related('room')

    if search_query:
        maintenances= maintenances.filter(
            Q(room__room_number__icontains=search_query) |
            Q(room__apartment__apartment_number__icontains=search_query)
        )

    if status_filter:
        maintenances = maintenances.filter(status__iexact=status_filter)

    paginator = Paginator(maintenances.order_by('date_reported'), 5)
    page_number = request.GET.get('page')
    maintenances_page = paginator.get_page(page_number)
    

    if request.method == 'POST' and 'submit_maintenance_reply' in request.POST:
        maintenance_id = request.POST.get('maintenance_id')
        reply_text = request.POST.get('reply', '').strip()
        new_status = request.POST.get('status')
        
        maintenance = get_object_or_404(MaintenanceRequest, id=maintenance_id)

        if reply_text and new_status in ['pending', 'in_progress', 'completed']:
            maintenance.reply = reply_text
            maintenance.status = new_status
            maintenance.save()
            messages.success(request, 'Reply and status updated successfully.')
            return redirect('maintenance')
        else:
            messages.error(request, 'Reply and valid status are required.')


    return render(request, 'my_admin_website/Adminmaintenance.html', {
        'maintenances': maintenances_page
    })
    

