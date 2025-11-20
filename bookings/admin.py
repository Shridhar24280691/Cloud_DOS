from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "email", "service_type", "preferred_date")
    search_fields = ("customer_name", "email", "license_plate")
    list_filter = ("service_type", "preferred_date")
