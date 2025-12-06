# cardetailing/urls.py
from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from django.contrib.auth import views as auth_views

from bookings import views as booking_views


@require_GET
def root_redirect(request):
    """Redirect root URL to the login page."""
    return redirect("login")


urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # Root → login
    path("", root_redirect, name="root_redirect"),

    # ========= AUTH =========
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="bookings/login.html"),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Signup (GET + POST separated for Sonar)
    path("accounts/signup/", booking_views.signup, name="signup"),
    path(
        "accounts/signup/submit/",
        booking_views.signup_submit,
        name="signup_submit",
    ),

    # ========= BOOKINGS =========
    # List
    path("bookings/", booking_views.booking_list, name="booking_list"),

    # Create
    path("bookings/create/", booking_views.create_booking, name="create_booking"),
    path(
        "bookings/create/submit/",
        booking_views.create_booking_submit,
        name="create_booking_submit",
    ),

    # Edit
    path("bookings/<int:pk>/edit/", booking_views.edit_booking, name="edit_booking"),
    path(
        "bookings/<int:pk>/edit/submit/",
        booking_views.edit_booking_submit,
        name="edit_booking_submit",
    ),

    # Delete
    path("bookings/<int:pk>/delete/", booking_views.delete_booking, name="delete_booking"),
    path(
        "bookings/<int:pk>/delete/confirm/",
        booking_views.delete_booking_confirm,
        name="delete_booking_confirm",
    ),

    # ========= HEALTH CHECK (EB) =========
    path("health/", booking_views.health, name="health"),
]
