from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from dashboard.views import *

# from dteams.views import delete_tdeam

urlpatterns = [
# ===================School========================,


    path("add_officer/", add_sports_officer, name="add_officer"),
    path("officer/<int:id>", officer_details, name="officerd"),
    path("deleteofficer/<int:id>", delete_officer, name="deleted"),
    path("officers/", officers, name="officers"),
    path("sports_officer_activate/<int:id>", activate_officer, name="dso_activate"),
    path("officeria/", Officerdash, name="officer_dashboard"),

    # email
    # path("enrolls_data/", enrolls_data, name="enrolls_data"),
    # path("teccred/", teccreditation, name="teccred"),
    path("dteam_accred/<int:id>", dAccreditation, name="dteam_accred"),
    path("dteam_album/<int:id>", dAlbums, name="dteam_album"),
    path("dteam_cert/<int:id>", dCertificate, name="dteam_cert"),
    path("district_enrollments/", district_teams, name="district_enrollments"),
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
    path("district_teams/", district_teams, name="district_teams"),

    # path("deledteam/<int:id>", delete_tdeam, name="deledteam"),
    path("Aofficers/", Aofficers, name="Aofficers"),
    # path("pdf_report/", generate_album, name="pdfreport"),
    # path("pdfreport/<int:id>", generate_scalbum, name="pdreport"),
    path("newtofficer/", newTofficer, name="districtoff"),
    path("tofficers/", team_officers, name="team_officers"),
    path("dofficers/", District_officers, name="dofficers"),
    path("newtofficer/<int:id>", tofficer_details, name="toff"),
    path("delete/tofficer/<int:id>", delete_tofficer, name="deltoff"),


    # ===================Athletes========================,
    path("district_schools/", district_schools, name="district_schools"),
    path("district_athletes/", district_athletes, name="district_athletes"),
    # path("editofficer/<int:id>", profile_update, name="editofficer"),
    # path("dacreditation/<int:id>", toAccreditation, name="tocrred"),
    # path("dacertification/<int:id>", toCertification, name="tocert"),
    # path("delete/enrollment/<int:id>", officer_enroll_delete, name="delteam"),
    
   # ===================Officials========================,


    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
