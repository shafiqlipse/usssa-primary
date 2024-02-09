from django.contrib import admin
from django.urls import path, include
from dashboard.views import *
from accounts.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", user_login, name="login"),
    path("register/", school_registration, name="register"),
    path("logout/", user_logout, name="logout"),
    path("dashboard/", Overview, name="dashboard"),
    path("school/", Dash, name="school_dashboard"),
    path("dashboard/", include("dashboard.urls")),
    path("get_zones/", get_zones, name="get_zones"),
]
