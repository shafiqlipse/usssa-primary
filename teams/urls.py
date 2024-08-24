from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *
from .teviews import *


urlpatterns = [
    #--------------------------------
    #  # team
    path("new_team/", create_team, name="new_team"),
    path("updateteam/<int:id>", update_team, name="updategteam"),
    path("teams/", teamlist, name="team_s"),
    path("allteams/", allteamlist, name="allteam_s"),
    path("team/<int:id>", team_details, name="steam"),
    path("activate_team/<int:id>", activate_team, name="activate_team"),
    path("deactivate_team/<int:id>", deactivate_team, name="deactivate_team"),
    path("sdalbum/<int:id>", generate_sdalbum, name="sdalbum"),
    path("team_accred/<int:id>", teamAccreditation, name="team_accred"),
    path("team_cert/<int:id>", TeamCert, name="team_cert"),
    path("deleteteam/<int:id>", delete_team, name="delete_team"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
