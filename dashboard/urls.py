from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from accounts.views import *
from core.views import *


urlpatterns = [
    # venues
    path("activate/<int:id>", activate_school, name="activate"),
    path("octivate/<int:id>", activate_officer, name="octivate"),
    path("schools/", schools, name="schools"),
    path("users/", users, name="users"),
    path("inactiveschools/", inactiveschools, name="inactiveschools"),
    path("activeschools/", activeschools, name="activeschools"),
    path("all_athletes/", all_athletes, name="athletex"),
    path("all_officials/", all_officials, name="all_officials"),
    path("tournaments/", Tournaments, name="tournaments"),
    path("districts/", districts, name="districts"),
    path("zones/", municipalities, name="zones"),
    path("addschool/", Schoolnew, name="new_school"),
    path("school/<int:id>", school_detail, name="schooldetail"),
    path("editschool/<int:id>", school_update, name="schoolupdate"),
    path("edit_school/<int:id>", schoolupdate, name="schoolpdate"),
    path("athletes", athletes, name="athletes"),
    path("officials", school_offs, name="officials"),
    path("athlete/<int:id>", AthleteDetail, name="athlete"),
    path("official/<int:id>", OfficialDetail, name="official"),
    path("updateathlete/<int:id>", AthleteUpdate, name="updateathlete"),
    path("deleteathlete/<int:id>", DeleteAthlete, name="delathlete"),
    path("deleteschool/<int:id>", DeleteSchool, name="delschool"),
    path("addathlete", newAthlete, name="addathlete"),
    path("addofficial", Official, name="addofficial"),
    # path("updateofficial/<int:id>", update_official, name="updateofficial"),
    # path("official/<int:id>", official_details, name="official"),
    # path("deleteofficial/<int:id>", delete_official, name="deleteofficial"),
    path("export-csv/", export_csv, name="export_csv"),
    path("exportp-csv/", exportp_csv, name="exportp_csv"),
    path("export-pdf/", export_pdf, name="export_pdf"),
    # competition
    path("athlete-list/", reg_athletes, name="athlete_list"),
    path("payment-page/", payment_page, name="payment_page"),
    path("album/", album, name="album"),
    path("dalbum/<int:id>", generate_dalbum, name="dalbum"),
    path("accred/<int:id>", accreditation, name="accred"),
    # path("process-payment/", process_payment, name="process_payment"),  # Add this line
    # Add more URLs as ne
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
