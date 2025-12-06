# bookings/tests/test_middleware.py
from django.http import HttpResponse
from django.test import RequestFactory, SimpleTestCase

from bookings.middleware import SecurityHeadersMiddleware


class SecurityHeadersMiddlewareTests(SimpleTestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

        # simple view that just returns "OK"
        def get_response(_request):
            return HttpResponse("OK")

        self.middleware = SecurityHeadersMiddleware(get_response)

    def test_security_headers_are_added(self):
        request = self.factory.get("/")
        response = self.middleware(request)

        # basic security headers
        self.assertEqual(response["X-Frame-Options"], "DENY")
        self.assertEqual(response["Referrer-Policy"], "same-origin")
        self.assertEqual(response["X-Content-Type-Options"], "nosniff")

        # Spectre / site isolation headers
        self.assertEqual(response["Cross-Origin-Opener-Policy"], "same-origin")
        self.assertEqual(response["Cross-Origin-Embedder-Policy"], "require-corp")
        self.assertEqual(response["Cross-Origin-Resource-Policy"], "same-origin")

        # CSP header
        self.assertIn("Content-Security-Policy", response)
        csp = response["Content-Security-Policy"]
        self.assertIn("default-src 'self'", csp)
        self.assertIn("style-src 'self' https://cdn.jsdelivr.net", csp)
