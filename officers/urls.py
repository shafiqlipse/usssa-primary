from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from dashboard.views import *

# from teams.views import delete_tdeam

urlpatterns = [
# ===================School========================,


    path("officer/", Officera, name="officer"),
    path("officer/<int:id>", officer_details, name="officerd"),
    path("deleteofficer/<int:id>", delete_officer, name="deleted"),
    path("officeria/", Officerdash, name="officer_dashboard"),

    path("get_dist_athletes/", get_dist_athletes, name="get_dist_athletes"),
    # path("enrollment/", include("registration.urls")),
    # email
    # path('send_email/', Sendmail, name='send_email'),
    path("teams/", Teams, name="teams"),
    path("allteams/", AllTeams, name="allteams"),
    path("newteam/", create_team, name="teamnew"),
    path("updateteam/<int:id>", update_team, name="updateteam"),
    path("team/<int:id>", team_details, name="team"),
    path("teamd/<int:id>", team_ddetails, name="dteam"),
    # path("deleteam/<int:id>", delete_tdeam, name="deleteam"),
    path("officers/", officers, name="officers"),
    # path("pdf_report/", generate_album, name="pdfreport"),
    # path("pdfreport/<int:id>", generate_scalbum, name="pdreport"),
    path("newtofficer/", newTofficer, name="districtoff"),
    path("tofficers/", tofficers, name="tofficers"),
    path("dofficers/", Dofficers, name="dofficers"),
    path("newtofficer/<int:id>", tofficer_details, name="toff"),
    path("deloff/<int:id>", delloff, name="deloff"),


    # ===================Athletes========================,
    path("district_schools/", district_schools, name="district_schools"),
    path("district_athletes/", district_athletes, name="district_athletes"),
    path("editofficer/<int:id>", profile_update, name="editofficer"),
    
   # ===================Officials========================,

    path("dalbum/<int:id>", generate_dalbum, name="dalbum"),
    path("accred/<int:id>", accreditation, name="accred"),
    path("taccred/<int:id>", taccreditation, name="taccred"),
    path("cert/<int:id>", cert, name="cert"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
