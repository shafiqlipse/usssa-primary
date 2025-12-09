from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from accounts.views import *



urlpatterns = [
path("dashboard/", Overview, name="dashboard"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
