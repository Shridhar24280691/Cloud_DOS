# bookings/tests/test_forms.py
from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase

from bookings.forms import BookingForm


class BookingFormCleanMethodsTests(SimpleTestCase):
    def test_clean_preferred_date_rejects_past_date(self):
        form = BookingForm()
        form.cleaned_data = {"preferred_date": date.today() - timedelta(days=1)}

        with self.assertRaises(ValidationError):
            form.clean_preferred_date()

    def test_clean_preferred_date_accepts_today_or_future(self):
        form = BookingForm()
        form.cleaned_data = {"preferred_date": date.today()}

        # should not raise
        form.clean_preferred_date()

    def test_clean_phone_rejects_invalid_number(self):
        form = BookingForm()
        # obviously invalid number, adapt if your validation is different
        form.cleaned_data = {"phone": "abc"}

        with self.assertRaises(ValidationError):
            form.clean_phone()

    def test_clean_phone_accepts_valid_number(self):
        form = BookingForm()
        form.cleaned_data = {"phone": "+353800500123"}

        # should not raise
        form.clean_phone()
