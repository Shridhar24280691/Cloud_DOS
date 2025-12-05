from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.views.decorators.http import require_GET
from bookings.views import health  # health-check endpoint


@require_GET
def root_redirect(request):
    """Always redirect / to the login page via safe GET."""
    return redirect("/accounts/login/")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", root_redirect, name="root_redirect"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("bookings/", include("bookings.urls")),
    path("health/", health, name="health"),
]
