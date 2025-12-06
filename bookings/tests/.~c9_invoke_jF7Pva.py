from datetime import date, timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from bookings.models import Booking


class SignupViewTests(TestCase):
    """Tests for the public signup views."""

    def test_signup_get_renders_template(self):
        """GET /signup/ returns the signup page with the correct template."""
        response = self.client.get(reverse("signup"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/signup.html")

    def test_signup_submit_creates_user_and_redirects(self):
        """POST /signup/submit/ creates a user and redirects to booking_list."""
        username = "newuser"

        response = self.client.post(
            reverse("signup_submit"),
            {
                "username": username,
                # UserCreationForm fields
                "password1": "StrongPass12345",
                "password2": "StrongPass12345",
            },
        )

        # success -> redirect to booking_list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("booking_list"))
        self.assertTrue(User.objects.filter(username=username).exists())


class BookingViewsTests(TestCase):
    """Tests for the booking CRUD views."""

    def setUp(self):
        # Base user used for most tests
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",  # test-only credential
        )

    # ---------- helpers ----------

    def _login(self, user=None, password="testpass123"):
        """Log in as the given user (or default self.user)."""
        user = user or self.user
        self.client.login(username=user.username, password=password)

    def _valid_booking_data(self, **overrides):
        """
        Return a dict with *valid* form data for BookingForm.

        ⚠️ IMPORTANT:
        - If your Booking.service_type choices are different, update
          the 'service_type' value to one of your valid keys or labels.
        - If preferred_time_slot is required and cannot be null, you will
          need to create a real time slot object and pass its PK here.
        """
        data = {
            "customer_name": "Test Customer",
            "email": "customer@example.com",
            "phone": "1234567890",
            "car_model": "Test Car",
            # TODO: adjust if your choices differ
            "service_type": "Full Detailing",
            "preferred_date": (date.today() + timedelta(days=1)).isoformat(),
            "preferred_time_slot": "",
            "notes": "Some notes from tests.",
        }
        data.update(overrides)
        return data

    def _create_booking_instance(self, owner=None):
        """
        Create a Booking instance directly, for edit/delete tests.

        ⚠️ If your Booking model has non-null constraints (for example,
        preferred_time_slot cannot be null), adapt this to create any
        related objects needed and pass them here.
        """
        owner = owner or self.user

        return Booking.objects.create(
            user=owner,
            customer_name="Existing Customer",
            email="existing@example.com",
            phone="9876543210",
            car_model="Existing Car",
            # keep consistent with _valid_booking_data
            service_type="Full Detailing",
            preferred_date=date.today() + timedelta(days=1),
            notes="Existing booking from tests.",
            # preferred_time_slot can be left as default/null if your model allows it.
        )

    # ---------- booking_list ----------

    def test_booking_list_requires_login(self):
        """Anonymous users are redirected to login for booking_list."""
        response = self.client.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_booking_list_for_normal_user_filters_by_user(self):
        """Non-staff users only see their own bookings."""
        # booking for self.user
        booking_own = self._create_booking_instance(owner=self.user)
        # booking for another user
        other = User.objects.create_user(
            username="other", password="otherpass123"
        )
        self._create_booking_instance(owner=other)

        self._login()
        response = self.client.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/booking_list.html")

        bookings = list(response.context["bookings"])
        self.assertEqual(bookings, [booking_own])

    def test_booking_list_for_staff_sees_all(self):
        """Staff users see all bookings."""
        staff = User.objects.create_user(
            username="staffuser", password="staffpass123", is_staff=True
        )
        b1 = self._create_booking_instance(owner=self.user)
        b2 = self._create_booking_instance(owner=staff)

        self._login(user=staff, password="staffpass123")
        response = self.client.get(reverse("booking_list"))
        self.assertEqual(response.status_code, 200)

        # Should see both bookings
        bookings = set(response.context["bookings"])
        self.assertEqual(bookings, {b1, b2})

    # ---------- create_booking (GET + POST) ----------

    def test_create_booking_get_renders_form(self):
        """GET /create/ renders the create booking form."""
        self._login()
        response = self.client.get(reverse("create_booking"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/booking_form.html")
        self.assertContains(response, "Create Booking")

    def test_create_booking_submit_invalid_shows_form_again(self):
        """
        POST /create/submit/ with invalid data should stay on the form.

        We intentionally send empty data so that form.is_valid() is False,
        exercising the POST branch that re-renders the template.
        """
        self._login()
        response = self.client.post(reverse("create_booking_submit"), {})

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/booking_form.html")
        self.assertContains(response, "Create Booking")

    # ---------- edit_booking (GET + POST) ----------

    def test_edit_booking_get_as_owner(self):
        """Owner can view the edit page for their booking."""
        booking = self._create_booking_instance()
        self._login()

        url = reverse("edit_booking", args=[booking.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/booking_form.html")
        self.assertContains(response, "Edit Booking")

    def test_edit_booking_submit_invalid_keeps_user_on_form(self):
        """
        POST /edit/<pk>/submit/ with invalid data should re-render form.

        Again we send clearly invalid data so is_valid() is False, but the
        POST code path is covered.
        """
        booking = self._create_booking_instance()
        self._login()

        url = reverse("edit_booking_submit", args=[booking.pk])
        response = self.client.post(url, {"customer_name": ""})  # invalid

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bookings/booking_form.html")
        self.assertContains(response, "Edit Booking")

    def test_edit_booking_forbidden_for_non_owner(self):
        """Non-owner non-staff users should receive 403 for edit_booking."""
        booking = self._create_booking_instance()

        other = User.objects.create_user(
            username="outsider", password="outsider123"
        )
        self._login(user=other, password="outsider123")

        url = reverse("edit_booking", args=[booking.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    # ---------- delete_booking (GET + POST) ----------

    def test_delete_booking_get_confirmation_page(self):
        """Owner sees a confirmation page before deletion."""
        booking = self._create_booking_instance()
        self._login()

        url = reverse("delete_booking", args=[booking.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "bookings/booking_confirm_delete.html"
        )
        self.assertContains(response, "Delete Booking")

    def test_delete_booking_confirm_deletes_and_redirects(self):
        """POST /delete/<pk>/confirm/ deletes the booking and redirects."""
        booking = self._create_booking_instance()
        self._login()

        url = reverse("delete_booking_confirm", args=[booking.pk])
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("booking_list"))
        self.assertFalse(
            Booking.objects.filter(pk=booking.pk).exists(),
            "Booking should be deleted after delete_booking_confirm POST",
        )

    def test_delete_booking_forbidden_for_non_owner(self):
        """Non-owner non-staff users cannot access delete_booking."""
        booking = self._create_booking_instance()
        other = User.objects.create_user(
            username="outsider_del", password="outsider456"
        )
        self._login(user=other, password="outsider456")

        url = reverse("delete_booking", args=[booking.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
