from django import forms
from datetime import date
from .models import Booking

class BookingForm(forms.ModelForm):
    
    preferred_date = forms.DateField(
    widget=forms.DateInput(attrs={"type": "date"})
    )

    preferred_time = forms.TimeField(
    widget=forms.TimeInput(attrs={"type": "time"})
    )

    
    
    class Meta:
        model = Booking
        fields = [
            "customer_name",
            "email",
            "phone",
            "car_model",
            "service_type",
            "preferred_date",
            "preferred_time",
            "notes",
        ]

    def clean_preferred_date(self):
        chosen_date = self.cleaned_data["preferred_date"]
        # Do not allow bookings in the past
        if chosen_date < date.today():
            raise forms.ValidationError("Preferred date cannot be in the past.")
        return chosen_date

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        # Basic validation for phone number length
        digits = [c for c in phone if c.isdigit()]
        if len(digits) < 7:
            raise forms.ValidationError("Phone number seems too short.")
        return phone
