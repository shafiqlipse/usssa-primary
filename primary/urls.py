from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from dashboard.views import *
from accounts.views import *
from core.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", user_login, name="login"),
    path("", home, name="home"),
    path("change_password/", change_password, name="change_password"),
    path("confirmation/", confirmation, name="confirmation"),
    path("register/", school_registration, name="register"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/", Overview, name="dashboard"),
    path("school/", Dash, name="school_dashboard"),
    path("dashboard/", include("dashboard.urls")),
    # email
    # path('send_email/', Sendmail, name='send_email'),
    path("pdf_report/", generate_album, name="pdfreport"),
    # path("album/", album, name="album"),
    path("select2/", include("django_select2.urls")),
    path("calculate_age_choices/", calculate_age_choices, name="calculate_age_choices"),
]  # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
