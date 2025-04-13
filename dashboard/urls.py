from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from .views import *
from accounts.views import *



urlpatterns = [

    path("users/", users, name="users"),
    path("staff/", staff, name="staff"),
    path("sports_officers/", sports_officers, name="sports_officers"),
    path('user/edit/<int:id>/', edit_user, name='edit_user'),
    path('users/data/', users_data, name='users_data'),
    path("tournaments/", Tournaments, name="tournaments"),
    # path("districts/", districts, name="districts"),
    # path("districts/", districts, name="districts"),

    # path("official/<int:id>", official_details, name="official"),


    # path("deleteofficial/<int:id>", delete_official, name="deleteofficial"),
    path("export-csv/", export_csv, name="export_csv"),
    path("exportp-csv/", exportp_csv, name="exportp_csv"),
    path("export-pdf/", export_pdf, name="export_pdf"),
    # competition

    path("album/", album, name="album"),

    # path("process-payment/", process_payment, name="process_payment"),  # Add this line
    # Add more URLs as ne
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
