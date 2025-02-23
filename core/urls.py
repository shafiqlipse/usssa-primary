from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from core.frontviews import *


urlpatterns = [
    # venues
    path("contact", contact, name="contact"),
    path("about", about, name="about"),
    path("schools", schooles, name="schooles"),
    path("faq", faq, name="faq"),
    
    # Add more URLs as ne
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
