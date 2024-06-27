from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *

from .views import *


urlpatterns = [
    # venues
    path("addteacher/", Teachera, name="addteacher"),
    # path("teccred/", teccreditation, name="teccred"),
    path("teachers/", Teachers, name="teachers"),
    path("teacher/<int:id>", teacher_details, name="teacher"),
    # path("process-payment/", process_payment, name="process_payment"),  # Add this line
    # Add more URLs as ne
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
