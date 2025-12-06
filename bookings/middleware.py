# bookings/middleware.py
class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Basic security headers
        response.setdefault("X-Frame-Options", "DENY")
        response.setdefault("Referrer-Policy", "same-origin")
        response.setdefault("X-Content-Type-Options", "nosniff")

        # Site isolation – helps with ZAP 90004
        response.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        response.setdefault("Cross-Origin-Embedder-Policy", "require-corp")
        response.setdefault("Cross-Origin-Resource-Policy", "same-origin")

        # CSP
        csp = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' https://cdn.jsdelivr.net; "
            "img-src 'self' https://images.unsplash.com data:; "
            "font-src 'self' data:; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        response.setdefault("Content-Security-Policy", csp)

        return response
