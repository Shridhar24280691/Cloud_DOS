from django.urls import path
from . import views
from .views import health

urlpatterns = [
    path("health/", health),
    path("booking_list/", views.booking_list, name="booking_list"),
    path("create/", views.create_booking, name="create_booking"),
    path("edit/<int:pk>/", views.edit_booking, name="edit_booking"),
    path("delete/<int:pk>/", views.delete_booking, name="delete_booking"),
    path("signup/", views.signup, name="signup"),
]
