from django.db import models
from accounts.models import User
from datetime import timedelta
from datetime import datetime, timedelta


class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)  # <-- new field
    # apartements_count = models.IntegerField()

    def __str__(self):
     return self.name

    
class Block(models.Model):
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE, related_name='blocks')
    name = models.CharField(max_length=50)  # e.g., "Block A", "Block 1"

    def  __str__(self):
        
     return f" {self.accommodation.name} - block {self.name}"    
class Apartment(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]
    ROOM_TYPES = (
        ('deluxe', 'Deluxe'),
        ('premium', 'Premium'),
    )

    
    # accommodation = models.ForeignKey(Accommodation,
    # on_delete=models.CASCADE,
    # related_name='apartments',
    # null=True,  # temporarily allow nulls
    # blank=True  )
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='apartments')
    apartment_number = models.CharField(max_length=10, unique=True)  
    type = models.CharField(max_length=10, choices=ROOM_TYPES, default='premium')
    level = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')



    def  __str__(self):
        return f"Accommodation {self.block} - Level {self.level} -  APT{self.apartment_number}"
   

class Room(models.Model):
    
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('inactive', 'Inactive'),
    )

    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10, primary_key=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
   
   

    def  __str__(self):
        return f"{self.apartment}-Room {self.room_number}"

class Booking(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('cancelled', 'Cancelled'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    def save(self, *args, **kwargs):
        if not self.expiration_date:
            booking_month = self.booking_date.month
            booking_year = self.booking_date.year

            # Semester 1: Sep - Jan → expires Feb 1
            if booking_month in [9, 10, 11, 12, 1]:
                # If booked in Jan, move expiration to Feb same year
                if booking_month == 1:
                    exp_year = booking_year
                else:
                    exp_year = booking_year + 1
                self.expiration_date = datetime(exp_year, 2, 1)#1/2

            # Semester 2: Feb - May → expires May 31
            elif booking_month in [2, 3, 4, 5]:
                self.expiration_date = datetime(booking_year, 5, 31)#5/31

            # Semester 3: Jul - Aug → expires Sep 1
            elif booking_month in [6,7, 8]:
                self.expiration_date = datetime(booking_year, 9, 1)#1/9


            else:
                self.expiration_date = self.booking_date + timedelta(days=90)

        super().save(*args, **kwargs)
    def  __str__(self):
        return f"Booking: {self.student} -> {self.room}"


class Complaint(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        
    )

    student = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    
    reply = models.TextField(blank=True, null=True)  

    def __str__(self):
        return f"Complaint by {self.student}: {self.subject}"


class MaintenanceRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    ISSUE_TYPE_CHOICES = [
        ('Water Leakage', 'Water Leakage'),
        ('Air Conditioner', 'Air Conditioner'),
        ('Electricity', 'Electricity'),
        ('Furniture', 'Furniture'),
        ('Others', 'Others'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=50, choices=ISSUE_TYPE_CHOICES, default='Others')
    description = models.TextField()
    date_reported = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    reply = models.TextField(blank=True, null=True)  # Admin reply field

    def __str__(self):
        return f"Maintenance in {self.room}: {self.issue_type}"

