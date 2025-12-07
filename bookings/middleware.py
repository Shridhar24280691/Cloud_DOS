# bookings/middleware.py
class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Basic security headers
        response.setdefault("X-Frame-Options", "DENY") # Prevents clickjacking by blocking the page from being embedded in iframes on other sites.
        response.setdefault("Referrer-Policy", "same-origin") # Limits referrer information sent to same-origin requests only, reducing data leakage risks.
        response.setdefault("X-Content-Type-Options", "nosniff")

        # Site isolation to prevent cross-origin attacks like Spectre – helps with ZAP 90004
        response.setdefault("Cross-Origin-Opener-Policy", "same-origin")
        response.setdefault("Cross-Origin-Embedder-Policy", "require-corp")
        response.setdefault("Cross-Origin-Resource-Policy", "same-origin")
        response.setdefault("Permissions-Policy","geolocation=(), microphone=(), camera=()",)
        # Content Security Policy (CSP)
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
