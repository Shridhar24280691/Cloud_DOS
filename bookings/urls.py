from django.urls import path
from . import views
from .views import health

urlpatterns = [
    path("", views.booking_list, name="booking_list"),

    # CREATE
    path("create/", views.create_booking, name="create_booking"),                 # GET
    path("create/submit/", views.create_booking_submit, name="create_booking_submit"),  # POST

    # EDIT
    path("<int:pk>/edit/", views.edit_booking, name="edit_booking"),             # GET
    path("<int:pk>/edit/submit/", views.edit_booking_submit, name="edit_booking_submit"),  # POST

    # DELETE
    path("<int:pk>/delete/", views.delete_booking, name="delete_booking"),       # GET
    path("<int:pk>/delete/confirm/", views.delete_booking_confirm, name="delete_booking_confirm"),  # POST
]
