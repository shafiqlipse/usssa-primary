from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

# from teams.views import delete_tdeam

urlpatterns = [



    # ===================School========================,

    
    # ===================Athletes========================,
 
    
   # ===================Officials========================,

    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
