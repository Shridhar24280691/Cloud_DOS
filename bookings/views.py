from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

from .models import Booking
from .forms import BookingForm   # assume you already have this
from django.contrib.auth.forms import UserCreationForm


# ---------- AUTH VIEWS (SIGNUP ONLY, LOGIN IS BUILT-IN) ----------

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optional: log in automatically
            from django.contrib.auth import login
            login(request, user)
            return redirect("booking_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


# ---------- BOOKING VIEWS ----------
@login_required
def booking_list(request):
    """
    Admin/staff see all bookings.
    Normal users see only their own bookings.
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
def create_booking(request):
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user          # link to current user
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
def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    # Only owner or admin can edit
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
def delete_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    # Only owner or admin can delete
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
