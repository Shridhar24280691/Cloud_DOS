class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Basic CSP 
        csp = (
            "default-src 'self'; "
            "script-src 'self' https://cdn.jsdelivr.net; "
            "style-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
            "img-src 'self' data: https://images.unsplash.com; "
            "font-src 'self' https://cdn.jsdelivr.net https://fonts.gstatic.com; "
            "connect-src 'self'; "
            "frame-ancestors 'none'; "
            "form-action 'self'; "
            "base-uri 'self'"
        )
        response["Content-Security-Policy"] = csp

        # Permissions Policy
        response["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=(), fullscreen=(), payment=()"
        )

        # Other helpful headers
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response["X-Content-Type-Options"] = "nosniff"
        response["X-Frame-Options"] = "DENY"

        return response
