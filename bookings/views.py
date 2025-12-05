from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_http_methods
from django.contrib.auth.forms import UserCreationForm

from .models import Booking
from .forms import BookingForm


@require_GET
def health(request):
    """Simple health-check endpoint used by Elastic Beanstalk."""
    return JsonResponse({"status": "ok"})


# ---------- AUTH VIEWS (SIGNUP ONLY, LOGIN IS BUILT-IN) ----------

@require_http_methods(["GET", "POST"])
def signup(request):
    """
    Public signup view.

    GET  -> return blank signup form.
    POST -> validate + create user, then redirect to booking list.
    """
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: log in automatically after signup
            from django.contrib.auth import login

            login(request, user)
            return redirect("booking_list")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


# ---------- BOOKING VIEWS ----------

@login_required
@require_GET
def booking_list(request):
    """
    Booking list.
    """
    if request.user.is_staff or request.user.is_superuser:
        bookings = Booking.objects.all().order_by("-preferred_date", "-preferred_time")
    else:
        bookings = Booking.objects.filter(user=request.user).order_by(
            "-preferred_date",
            "-preferred_time",
        )

    return render(request, "bookings/booking_list.html", {"bookings": bookings})


@login_required
@require_http_methods(["GET", "POST"])
def create_booking(request):
    """
    GET  -> show booking creation form.
    POST -> create a new booking for the logged-in user.
    """
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user  # link to current user
            booking.save()
            return redirect("booking_list")
    else:
        # Optionally pre-fill name/email from user
        initial = {}
        if request.user.get_full_name():
            initial["customer_name"] = request.user.get_full_name()
        else:
            initial["customer_name"] = request.user.username

        if request.user.email:
            initial["email"] = request.user.email

        form = BookingForm(initial=initial)

    return render(
        request,
        "bookings/booking_form.html",
        {"form": form, "title": "Create Booking"},
    )


@login_required
@require_http_methods(["GET", "POST"])
def edit_booking(request, pk):
    """
    GET  -> show edit form.
    POST -> save edits for the booking if owner or staff.
    """
    booking = get_object_or_404(Booking, pk=pk)

    if not (request.user.is_staff or booking.user == request.user):
        raise PermissionDenied

    if request.method == "POST":
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect("booking_list")
    else:
        form = BookingForm(instance=booking)

    return render(
        request,
        "bookings/booking_form.html",
        {"form": form, "title": "Edit Booking"},
    )


@login_required
@require_http_methods(["GET", "POST"])
def delete_booking(request, pk):
    """
    GET  -> show delete confirmation page.
    POST -> actually delete the booking (CSRF-protected form).
    """
    booking = get_object_or_404(Booking, pk=pk)

    if not (request.user.is_staff or booking.user == request.user):
        raise PermissionDenied

    if request.method == "POST":
        booking.delete()
        return redirect("booking_list")

    return render(
        request,
        "bookings/booking_confirm_delete.html",
        {"booking": booking},
    )
