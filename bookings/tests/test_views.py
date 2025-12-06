# bookings/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class SignupViewTests(TestCase):
    def test_signup_get_renders_template(self):
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/signup.html")


class BookingViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    def test_booking_list_requires_login(self):
        response = self.client.get(reverse("booking_list"))
        # redirects to login page
        self.assertEqual(response.status_code, 302)

    def test_booking_list_authenticated(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/booking_list.html")

    def test_create_booking_get(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("create_booking"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/booking_form.html")
        self.assertContains(response, "Create Booking")
