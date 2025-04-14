from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from dashboard.views import *

# from dteams.views import delete_tdeam

urlpatterns = [
# ===================School========================,


    path("officer/", Officera, name="officer"),
    path("officer/<int:id>", officer_details, name="officerd"),
    path("deleteofficer/<int:id>", delete_officer, name="deleted"),
    path("officeria/", Officerdash, name="officer_dashboard"),

    # path("enrollment/", include("registration.urls")),
    # email
    #    path("enrolls_data/", enrolls_data, name="enrolls_data"),
    # path("teccred/", teccreditation, name="teccred"),
    path("dteam_accred/<int:id>", dAccreditation, name="dteam_accred"),
    path("dteam_album/<int:id>", dAlbums, name="dteam_album"),
    path("dteam_cert/<int:id>", dCertificate, name="dteam_cert"),
    path("district_enrollments/", dTeams, name="district_enrollments"),
    path("all_denrollments/", dAllEnrollments, name="all_denrollments"),
    path(
        "officer_enrollment/<int:id>",
        officer_enrollment_details,
        name="district_enrollment",
    ),
    path(
        "delete_officer_enrollment/<int:id>",
        officer_enroll_delete,
        name="delete_officer_enrollment",
    ),
    path(
        "update_officer_enrollment/<int:id>",
        officer_enrollment_update,
        name="update_officer_enrollment",
    ),
    path(
        "remove-athlete/<int:enrollment_id>/<int:athlete_id>/",
        remove_athlete,
        name="remove_athlete",
    ),
    # path('send_email/', Sendmail, name='send_email'),
    path("dteams/", dTeams, name="dteams"),

    # path("deledteam/<int:id>", delete_tdeam, name="deledteam"),
    path("officers/", officers, name="officers"),
    path("Aofficers/", Aofficers, name="Aofficers"),
    # path("pdf_report/", generate_album, name="pdfreport"),
    # path("pdfreport/<int:id>", generate_scalbum, name="pdreport"),
    path("newtofficer/", newTofficer, name="districtoff"),
    path("tofficers/", tofficers, name="tofficers"),
    path("dofficers/", Dofficers, name="dofficers"),
    path("newtofficer/<int:id>", tofficer_details, name="toff"),
    path("delete/tofficer/<int:id>", delete_tofficer, name="deltoff"),


    # ===================Athletes========================,
    path("district_schools/", district_schools, name="district_schools"),
    path("district_athletes/", district_athletes, name="district_athletes"),
    path("editofficer/<int:id>", profile_update, name="editofficer"),
    path("dacreditation/<int:id>", toAccreditation, name="tocrred"),
    
   # ===================Officials========================,


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
