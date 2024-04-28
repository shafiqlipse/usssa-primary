# middleware.py
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import render

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if settings.MAINTENANCE_MODE:
            # If maintenance mode is enabled, serve maintenance page
            return render(request, 'maintenance.html')
        else:
            # If maintenance mode is not enabled, proceed with request as usual
            response = self.get_response(request)
            return response
