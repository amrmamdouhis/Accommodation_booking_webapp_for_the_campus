from django.contrib import admin
from .models import Apartment, Room, Booking, Complaint, MaintenanceRequest, Accommodation, Block ,User

# Show apartments inline under Accommodation
# @admin.register(Accommodation)
# class AccommodationAdmin(admin.ModelAdmin):
#     list_display = ('name', 'location')  # Adjust according to your fields
    
# @admin.register(Apartment)
# class ApartmentAdmin(admin.ModelAdmin):
#     list_display = ('block', 'level')
#     search_fields = ('block',)


@admin.register(Accommodation)
class AccommodationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'accommodation')
    search_fields = ('name',)
    list_filter = ('accommodation',)

# @admin.register(Apartment)
# class ApartmentAdmin(admin.ModelAdmin):
#     list_display = ('apartment_number', 'block', 'level', 'room_count', 'status')
#     search_fields = ('apartment_number', 'block')
#     list_filter = ('status', 'block')
@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['apartment_number', 'block', 'level','type', 'status']
    search_fields = ['apartment_number', 'block__name']
    list_filter = ['block__accommodation', 'status','type']



@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'apartment','status')
    list_filter = ('status', 'apartment')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('student', 'room', 'booking_date','expiration_date', 'status')
    list_filter = ('status',)
    search_fields = ('student_name', 'room_room_number')  # corrected fields with double underscores

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = User.objects.filter(role='student')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
from django.contrib import admin
from .models import MaintenanceRequest, Complaint

@admin.register(MaintenanceRequest)
class MaintenanceRequestAdmin(admin.ModelAdmin):
    list_display = ('room', 'issue_type', 'status', 'date_reported', 'reply_preview')
    list_filter = ('status', 'issue_type')
    search_fields = ('room__room_number', 'issue_type', 'description', 'reply')
    readonly_fields = ('date_reported',)

    def reply_preview(self, obj):
        return (obj.reply[:75] + '...') if obj.reply else '-'
    reply_preview.short_description = 'Reply'

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'status', 'date','reply_preview')
    list_filter = ('status',)
    search_fields = ('student__name', 'subject', 'description')
    readonly_fields = ('date',)
    def reply_preview(self, obj):
        return (obj.reply[:75] + '...') if obj.reply else '-'
    reply_preview.short_description = 'Reply'
