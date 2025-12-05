from django.db import models
from django.contrib.auth.models import User


class TimeSlot(models.Model):
    """Admin-created time slots that customers can select from."""
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot = models.CharField(max_length=20, unique=True)
    def __str__(self):
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}"


class Booking(models.Model):
    SERVICE_CHOICES = [
        ("Interior Detailing", "Interior Detailing"),
        ("Exterior Detailing", "Exterior Detailing"),
        ("Full Detailing", "Full Detailing"),
        ("Ceramic Coating", "Ceramic Coating"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    car_model = models.CharField(max_length=255)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    preferred_date = models.DateField()
    preferred_time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT)

    notes = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.service_type} on {self.preferred_date}"
