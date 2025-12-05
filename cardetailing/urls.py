from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from django.contrib.auth import views as auth_views
from bookings import views as booking_views


@require_GET
def root_redirect(request):
    """Redirect root URL to login page."""
    return redirect("login")


urlpatterns = [
    path("admin/", admin.site.urls),

    # Root redirect
    path("", root_redirect, name="root_redirect"),

    # AUTH
    # Override Django's login view → use your template bookings/login.html
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="bookings/login.html"),
        name="login",
    ),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),

    # Custom signup view from bookings app
    path("accounts/signup/", booking_views.signup, name="signup"),

    # Booking pages
    path("bookings/", include("bookings.urls")),

    # EB Health check
    path("health/", booking_views.health, name="health"),
]
