from django.contrib import admin
from django.urls import path, include
from dashboard.views import *
from accounts.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", user_login, name="login"),
    path('change_password/', change_password, name='change_password'),
    # path("login/", user_login, name="login"),
    path("register/", school_registration, name="register"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/", Overview, name="dashboard"),
    path("school/", Dash, name="school_dashboard"),
    path("dashboard/", include("dashboard.urls")),

    path("calculate_age_choices/", calculate_age_choices, name="calculate_age_choices"),
]
