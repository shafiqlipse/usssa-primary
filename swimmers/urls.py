from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *


urlpatterns = [
    # venues
    path("addswimmer/", swimmera, name="addswimmer"),
    # path("teccred/", teccreditation, name="teccred"),
    path("swimmers/", swimmers, name="swimmers"),
    path("swimmer/<int:id>", swimmer_details, name="swimmer"),
    path("delswimmer/<int:id>", delete_swimmer, name="del_swimmer"),
    # path("process-payment/", process_payment, name="process_payment"),  # Add this line
    # Add more URLs as ne
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
