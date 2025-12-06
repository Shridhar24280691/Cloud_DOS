# bookings/tests/test_views.py
from datetime import date

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse

from bookings.forms import BookingForm


class PublicViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()

    def test_root_redirects_to_login(self):
        """Root URL should redirect to the login page."""
        response = self.client.get(reverse("root_redirect"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_health_endpoint(self):
        """Health endpoint should return JSON with status ok."""
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})

    def test_signup_get_renders_form(self):
        """GET /accounts/signup/ should render the signup form."""
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_signup_post_invalid_shows_errors(self):
        """
        POST /accounts/signup/submit/ with invalid data
        should re-render the form with errors.
        """
        response = self.client.post(reverse("signup_submit"), data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)

    def test_signup_post_valid_creates_user_and_redirects(self):
        """Valid signup should create a new user and redirect to booking_list."""
        data = {
            "username": "newuser",
            "password1": "VeryStrongPass123!",
            "password2": "VeryStrongPass123!",
        }
        response = self.client.post(reverse("signup_submit"), data=data)
        # should redirect on success
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], reverse("booking_list"))
        self.assertTrue(User.objects.filter(username="newuser").exists())


class AuthenticatedBookingViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.user = User.objects.create_user(
            username="normal_user", password="secret123"
        )
        self.staff = User.objects.create_user(
            username="staff_user", password="secret123", is_staff=True
        )

    def test_booking_list_requires_login(self):
        """Anonymous users should be redirected to login."""
        response = self.client.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_booking_list_for_normal_user(self):
        """
        Logged-in non-staff user should see booking_list page
        (even if there are no bookings yet).
        """
        self.client.login(username="normal_user", password="secret123")
        response = self.client.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("bookings", response.context)

    def test_booking_list_for_staff_user(self):
        """Staff user should also see booking_list page."""
        self.client.login(username="staff_user", password="secret123")
        response = self.client.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("bookings", response.context)

    def test_create_booking_get_renders_form(self):
        """
        GET /bookings/create/ should render the booking form
        and set the correct post_url in the context.
        """
        self.client.login(username="normal_user", password="secret123")
        response = self.client.get(reverse("create_booking"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], BookingForm)
        self.assertEqual(response.context["title"], "Create Booking")
        self.assertEqual(
            response.context["post_url"], reverse("create_booking_submit")
        )

    def test_create_booking_post_invalid_shows_form_again(self):
        """
        POST /bookings/create/submit/ with invalid data should re-render
        the form with validation errors (covers the POST view path).
        """
        self.client.login(username="normal_user", password="secret123")
        response = self.client.post(reverse("create_booking_submit"), data={})
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertTrue(response.context["form"].errors)
