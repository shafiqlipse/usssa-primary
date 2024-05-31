from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [

  
    # # team
    path("new_team/", create_team, name="new_team"),
    path("updateteam/<int:id>", update_team, name="updateteam"),
    path("teams/", teamlist, name="team_s"),
    path("team/<int:id>", team_details, name="steam"),
    path("sdalbum/<int:id>", generate_sdalbum, name="sdalbum"),
    path("deleteteam/<int:id>", delete_team, name="deleteteam"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
