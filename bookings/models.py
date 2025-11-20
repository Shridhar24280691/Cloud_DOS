from django.db import models
from django.conf import settings

class Booking(models.Model):
    # Link each booking to a Django user
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookings",
        null=True,  
        blank=True
    )

    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    car_model = models.CharField(max_length=100)

    SERVICE_CHOICES = [
        ("exterior", "Exterior Detailing"),
        ("interior", "Interior Detailing"),
        ("full", "Full Detailing"),
    ]
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)

    preferred_date = models.DateField()
    preferred_time = models.TimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.customer_name} - {self.service_type} - {self.preferred_date}"
