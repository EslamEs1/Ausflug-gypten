"""
Booking forms for AusflugAgypten
"""

from django import forms
from .models import Booking


class BookingInquiryForm(forms.ModelForm):
    """Simple booking inquiry form"""
    
    date = forms.DateField(
        label="Datum",
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'input-field',
            'required': True,
        })
    )
    
    persons = forms.IntegerField(
        label="Anzahl Personen",
        min_value=1,
        max_value=50,
        initial=2,
        widget=forms.NumberInput(attrs={
            'class': 'input-field',
            'required': True,
        })
    )
    
    name = forms.CharField(
        label="Name",
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': 'Ihr Name',
            'required': True,
        })
    )
    
    email = forms.EmailField(
        label="E-Mail",
        widget=forms.EmailInput(attrs={
            'class': 'input-field',
            'placeholder': 'ihre@email.com',
            'required': True,
        })
    )
    
    phone = forms.CharField(
        label="Telefon",
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'input-field',
            'placeholder': '+49 ',
            'required': True,
        })
    )
    
    special_requests = forms.CharField(
        label="Besondere Wünsche",
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'input-field',
            'rows': 3,
            'placeholder': 'Haben Sie besondere Wünsche oder Fragen?',
        })
    )
    
    class Meta:
        model = Booking
        fields = ['date', 'persons', 'name', 'email', 'phone', 'special_requests']
    
    def __init__(self, *args, **kwargs):
        self.tour = kwargs.pop('tour', None)
        self.excursion = kwargs.pop('excursion', None)
        self.activity = kwargs.pop('activity', None)
        self.transfer = kwargs.pop('transfer', None)
        super().__init__(*args, **kwargs)
    
    def clean_date(self):
        date = self.cleaned_data['date']
        from datetime import date as dt_date
        if date < dt_date.today():
            raise forms.ValidationError("Das Datum muss in der Zukunft liegen.")
        return date
    
    def save(self, commit=True):
        booking = super().save(commit=False)
        
        # Set customer details
        booking.customer_name = self.cleaned_data['name']
        booking.customer_email = self.cleaned_data['email']
        booking.customer_phone = self.cleaned_data['phone']
        booking.booking_date = self.cleaned_data['date']
        booking.number_of_participants = self.cleaned_data['persons']
        booking.special_requests = self.cleaned_data.get('special_requests', '')
        
        # Set tour/excursion/activity/transfer
        if self.tour:
            booking.tour = self.tour
            booking.excursion = None
            booking.activity = None
            booking.transfer = None
            booking.total_price = self.tour.price * booking.number_of_participants
        elif self.excursion:
            booking.excursion = self.excursion
            booking.tour = None
            booking.activity = None
            booking.transfer = None
            booking.total_price = self.excursion.price * booking.number_of_participants
        elif self.activity:
            booking.activity = self.activity
            booking.tour = None
            booking.excursion = None
            booking.transfer = None
            booking.total_price = self.activity.price * booking.number_of_participants
        elif self.transfer:
            booking.transfer = self.transfer
            booking.tour = None
            booking.excursion = None
            booking.activity = None
            # For transfers, price might be per vehicle, not per person
            if hasattr(self.transfer, 'price_per_person') and self.transfer.price_per_person:
                booking.total_price = self.transfer.display_price * booking.number_of_participants
            else:
                booking.total_price = self.transfer.display_price
        
        # Set status to pending
        booking.status = 'pending'
        
        if commit:
            booking.save()
        
        return booking

