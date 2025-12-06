from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse

from .models import Booking
from .forms import BookingForm

# ===== Template path constants =====
BOOKING_FORM_TEMPLATE = "bookings/booking_form.html"
SIGNUP_TEMPLATE = "bookings/signup.html"


def _render_booking_form(request, form, title, post_url):
    """
    Internal helper to render the booking form.

    Keeping this in one place avoids duplication and keeps
    SonarQube happy about repeated code blocks.
    """
    context = {
        "form": form,
        "title": title,
        "post_url": post_url,
    }
    return render(request, BOOKING_FORM_TEMPLATE, context)


@require_GET
def health(request):
    """Simple health-check endpoint used by Elastic Beanstalk."""
    return JsonResponse({"status": "ok"})


# ---------- AUTH VIEWS ----------

@require_GET
def signup(request):
    """
    Public signup view (GET only).
    Returns a blank signup form.
    """
    form = UserCreationForm()
    return render(request, SIGNUP_TEMPLATE, {"form": form})


@require_POST
def signup_submit(request):
    """
    Handles signup form submission (POST only).
    Creates a new user and redirects to booking list.
    """
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("booking_list")

    # invalid -> show form again with errors
    return render(request, SIGNUP_TEMPLATE, {"form": form})


# ---------- BOOKING VIEWS ----------

@login_required
@require_GET
def booking_list(request):
    """
    Booking list (GET only).
    """
    if request.user.is_staff or request.user.is_superuser:
        bookings = Booking.objects.all().order_by(
            "-preferred_date", "-preferred_time_slot__start_time"
        )
    else:
        bookings = Booking.objects.filter(user=request.user).order_by(
            "-preferred_date",
            "-preferred_time_slot__start_time",
        )

    return render(request, "bookings/booking_list.html", {"bookings": bookings})


@login_required
@require_GET
def create_booking(request):
    """
    GET -> show booking creation form.
    """
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
        {
            "form": form,
            "title": "Create Booking",
            "post_url": reverse("create_booking_submit"),  # IMPORTANT
        },
    )


@login_required
@require_POST
def create_booking_submit(request):
    """
    POST -> create a new booking for the logged-in user.
    (No side effects on GET, which is what SonarQube expects.)
    """
    form = BookingForm(request.POST)
    if form.is_valid():
        booking = form.save(commit=False)
        booking.user = request.user
        booking.save()
        return redirect("booking_list")

    # Invalid form -> show again
    return _render_booking_form(
        request,
        form=form,
        title="Create Booking",
        post_url=reverse("create_booking_submit"),
    )


@login_required
@require_GET
def edit_booking(request, pk):
    """
    GET -> show edit form.
    """
    booking = get_object_or_404(Booking, pk=pk)

    if not (request.user.is_staff or booking.user == request.user):
        raise PermissionDenied

    form = BookingForm(instance=booking)

    return _render_booking_form(
        request,
        form=form,
        title="Edit Booking",
        post_url=reverse("edit_booking_submit", args=[booking.pk]),
    )


@login_required
@require_POST
def edit_booking_submit(request, pk):
    """
    POST -> save edits for the booking if owner or staff.
    """
    booking = get_object_or_404(Booking, pk=pk)

    if not (request.user.is_staff or booking.user == request.user):
        raise PermissionDenied

    form = BookingForm(request.POST, instance=booking)
    if form.is_valid():
        form.save()
        return redirect("booking_list")

    return _render_booking_form(
        request,
        form=form,
        title="Edit Booking",
        post_url=reverse("edit_booking_submit", args=[booking.pk]),
    )


@login_required
@require_GET
def delete_booking(request, pk):
    """
    GET -> show delete confirmation page.
    """
    booking = get_object_or_404(Booking, pk=pk)

    if not (request.user.is_staff or booking.user == request.user):
        raise PermissionDenied

    return render(
        request,
        "bookings/booking_confirm_delete.html",
        {
            "booking": booking,
            "post_url": reverse("delete_booking_confirm", args=[booking.pk]),
        },
    )


@login_required
@require_POST
def delete_booking_confirm(request, pk):
    """
    POST -> actually delete the booking (CSRF-protected form).
    """
    booking = get_object_or_404(Booking, pk=pk)

    if not (request.user.is_staff or booking.user == request.user):
        raise PermissionDenied

    booking.delete()
    return redirect("booking_list")
