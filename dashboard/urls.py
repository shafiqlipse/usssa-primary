from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from accounts.views import *
from core.views import *


urlpatterns = [

    path("users/", users, name="users"),

    path("tournaments/", Tournaments, name="tournaments"),
    path("districts/", districts, name="districts"),
    # path("districts/", districts, name="districts"),

    # path("official/<int:id>", official_details, name="official"),
    path("district_schools/", district_schools, name="district_schools"),
    path("district_athletes/", district_athletes, name="district_athletes"),
    path("editofficer/<int:id>", profile_update, name="editofficer"),

    # path("deleteofficial/<int:id>", delete_official, name="deleteofficial"),
    path("export-csv/", export_csv, name="export_csv"),
    path("exportp-csv/", exportp_csv, name="exportp_csv"),
    path("export-pdf/", export_pdf, name="export_pdf"),
    # competition

    path("album/", album, name="album"),
    path("dalbum/<int:id>", generate_dalbum, name="dalbum"),
    path("accred/<int:id>", accreditation, name="accred"),
    path("taccred/<int:id>", taccreditation, name="taccred"),
    path("cert/<int:id>", cert, name="cert"),
    # path("process-payment/", process_payment, name="process_payment"),  # Add this line
    # Add more URLs as ne
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
