from django.urls import path
from . import views
from .views import health

urlpatterns = [
    path("health/", health),

    # bookings
    path("booking_list/", views.booking_list, name="booking_list"),

    path("create/", views.create_booking, name="create_booking"),
    path("create/submit/", views.create_booking_submit, name="create_booking_submit"),

    path("edit/<int:pk>/", views.edit_booking, name="edit_booking"),
    path(
        "edit/<int:pk>/submit/",
        views.edit_booking_submit,
        name="edit_booking_submit",
    ),

    path("delete/<int:pk>/", views.delete_booking, name="delete_booking"),
    path(
        "delete/<int:pk>/confirm/",
        views.delete_booking_confirm,
        name="delete_booking_confirm",
    ),

    # signup
    path("signup/", views.signup, name="signup"),
    path("signup/submit/", views.signup_submit, name="signup_submit"),
]
