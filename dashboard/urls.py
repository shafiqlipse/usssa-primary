from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    # venues
    path("schools/", schools, name="schools"),
    path("tournaments/", Tournaments, name="tournaments"),
    path("districts/", districts, name="districts"),
    path("zones/", zones, name="zones"),
    path("addschool/", Schoolnew, name="new_school"),
    path("school/<int:id>", school_detail, name="schooldetail"),
    path("athletes", athletes, name="athletes"),
    path("athlete/<int:id>", AthleteDetail, name="athlete"),
    path("addathlete", newAthlete, name="addathlete"),
    # path("updateofficial/<int:id>", update_official, name="updateofficial"),
    # path("official/<int:id>", official_details, name="official"),
    # path("deleteofficial/<int:id>", delete_official, name="deleteofficial"),
    # path("officials/", officials, name="officials"),
    # competition
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
