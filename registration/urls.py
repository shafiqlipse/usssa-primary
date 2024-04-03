from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from accounts.views import *


urlpatterns = [
    # venues
    path("enroll/<int:id>", enroll_school, name="enschool"),
    path("Tourns/", competition_list, name="tourns"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
