
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path("login/", user_login, name="login"),
    path("change_password/", change_password, name="change_password"),
    path("logout/", user_logout, name="logout"),

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
    #user management
    path("users_data/", users_data, name="users_data"),
    path("users/", users, name="users"),
    path('user/edit/<int:id>/', edit_user, name='edit_user'),
    path("staff/", staff, name="staff"),
    path("sports-officers/", sports_officers, name="xsports_officers"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 


# + debug_toolbar_urls()
