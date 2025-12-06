class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # XSS Protection
        response["X-XSS-Protection"] = "1; mode=block"

        # Prevent MIME sniffing
        response["X-Content-Type-Options"] = "nosniff"

        # Prevent clickjacking
        response["X-Frame-Options"] = "DENY"

        # Permissions Policy
        response["Permissions-Policy"] = (
            "camera=(), microphone=(), geolocation=()"
        )

        # Cross-Origin opener & resource isolation — fixes Spectre warnings
        response["Cross-Origin-Opener-Policy"] = "same-origin"
        response["Cross-Origin-Resource-Policy"] = "same-origin"
        response["Cross-Origin-Embedder-Policy"] = "require-corp"

        # OPTIONAL CSP to prevent 10038/10055
        response["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' https://images.unsplash.com data:; "
            "style-src 'self' 'unsafe-inline'; "
            "script-src 'self'; "
        )

        return response
