from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def root_redirect(request):
    return redirect("accounts/login")
    
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', root_redirect),   # always redirect root URL to login
    path('accounts/', include('django.contrib.auth.urls')),
    path('bookings/', include('bookings.urls')),
]
