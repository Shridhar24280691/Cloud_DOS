class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        response["Content-Security-Policy"] = (
            "default-src 'self'; "
            "img-src 'self' https://images.unsplash.com data:; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "script-src 'self'; "
        )

        # 2. Permissions-Policy
        response["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"

        # 3. Referrer-Policy
        response["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # 4. X-Content-Type-Options
        response["X-Content-Type-Options"] = "nosniff"

        # 5. Sec-Fetch-Dest synthetic fix
        response.setdefault("Sec-Fetch-Dest", "document")

        return response
