from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
# from debug_toolbar.toolbar import debug_toolbar_urls
from dashboard.views import *
from accounts.views import *
from core.views import *
from officers.views import *
from teams.teviews import get_athletes
# from teams.views import delete_tdeam

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", user_login, name="login"),
    path("", home, name="home"),
    path("change_password/", change_password, name="change_password"),
    path("confirmation/", confirmation, name="confirmation"),
    path("offcom/", offcom, name="offcom"),
    path("ofifcom/", ofifcom, name="ofifcom"),
    path("register/", school_registration, name="register"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/", Overview, name="dashboard"),
    path("officeria/", Officerdash, name="officer_dashboard"),
       # path("enrollment/", include("registration.urls")),
    # email
    # path('send_email/', Sendmail, name='send_email'),
    path("dashboard/", include("dashboard.urls")),
    path("team/", include("teams.urls")),
    path("core/", include("core.urls")),
    path("school/", include("school.urls")),
    path("officers/", include("officers.urls")),

    path("get_athletes/", get_athletes, name="get_athletes"),
    # path("enrollment/", include("registration.urls")),
    # email
    # path('send_email/', Sendmail, name='send_email'),

    path("pdf_report/", generate_album, name="pdfreport"),
    # path("pdfreport/<int:id>", generate_scalbum, name="pdreport"),
    # path("get_athletes/", get_athletes, name="get_athletes"),
    # path("album/", album, name="album"),
    path("select2/", include("django_select2.urls")),
    path("calculate_age_choices/", calculate_age_choices, name="calculate_age_choices"),
    path("password-reset/", ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    #
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
# + debug_toolbar_urls()
