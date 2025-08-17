import pycountry
from django import forms
from accounts.models import User
from .models import Apartment, Accommodation, Apartment, Block  # Adjust the model import path accordingly
from .models import Booking, User, Room



class AddStudentForm(forms.ModelForm):
    PROGRAM_CHOICES = [
        ('CS', 'Computer Science'),
        ('IS', 'Information Systems'),
        ('IT', 'Information Technology'),
        ('AI', 'Artificial Intelligence'),
        ('DS', 'Data Science'),
    ]

    # Generate country choices using pycountry
    COUNTRY_CHOICES = sorted([(country.name, country.name) for country in pycountry.countries])

    user_id = forms.CharField(
        max_length=10,
        min_length=10,
        label="Student ID",
        help_text="Must be exactly 10 characters.",
        widget=forms.TextInput(attrs={'placeholder': 'Enter 10 characters student ID'})
    )
    name = forms.CharField(
        max_length=255,
        label="Full Name",
        widget=forms.TextInput(attrs={'placeholder': 'Enter student name'})
    )
    program = forms.ChoiceField(choices=PROGRAM_CHOICES)
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)

    class Meta:
        model = User
        fields = ['user_id', 'name', 'country', 'program']

    def clean_user_id(self):
        user_id = self.cleaned_data['user_id']
        if len(user_id) != 10 :
            raise forms.ValidationError("Student ID must be exactly 10 digits.")
        return user_id

    def save(self, commit=True):
        student = super().save(commit=False)
        student.role = 'student'
        student.email = f"{student.user_id}@uniten.edu"
        student.set_password("uni10pass!")
        if commit:
            student.save()
        return student
    



class ApartmentForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=Apartment.ROOM_TYPES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Apartment Room Type'
    )

    block = forms.ModelChoiceField(
        queryset=Block.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label="Select a block"
    )

    class Meta:
        model = Apartment
        fields = ['block', 'apartment_number', 'level', 'status', 'type']
        widgets = {
            'apartment_number': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

class AccommodationForm(forms.ModelForm):
    number_of_blocks = forms.IntegerField(min_value=1, label="Number of Blocks")
    class Meta:
        model = Accommodation
        fields = ['name', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
from django import forms
from .models import Apartment

class ApartmentEditForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['block', 'apartment_number', 'level', 'status']
# forms.py





from django import forms
from .models import Booking, User, Room

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['student','status']  # exclude booking_date & expiration_date

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(role='student')
        self.fields['student'].label_from_instance = lambda obj: f"{obj.name} ({obj.user_id})"
        self.fields['student'].widget.attrs.update({'class': 'form-select'})

      
        self.fields['status'].widget.attrs.update({'class': 'form-select'})
        
from django import forms
from .models import Complaint

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['subject', 'description']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ComplaintReplyForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['reply']
        widgets = {
            'reply': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }



