from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from accounts.decorators import school_required, anonymous_required, staff_required
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib import messages
from .forms import SchoolRegistrationForm


@staff_required
def school_registration(request):
    if request.method == "POST":
        form = SchoolRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(
                commit=False
            )  # Create the user object without saving to the database
            user.is_school = True  # Set is_school to True
            user.save()  # Save the user object with is_school set to True

            # Log in the user
            login(request, user)

            return redirect("schools")
    else:
        form = SchoolRegistrationForm()
    return render(request, "register.html", {"form": form})


# Create your views here.
@anonymous_required
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Get the user without logging in
            user = form.get_user()
            login(request, user)

            # Check if the user is a school
            if user.is_school:
                # Check if the school user has a profile

                return redirect(
                    "school_dashboard"
                )  # Adjust the URL name for your create school profile view

            # If the user is not a school, log in and redirect to dashboard
            messages.success(request, "Login successful.")
            return redirect("dashboard")  # Adjust the URL name for your dashboard view
        else:
            messages.error(request, "Error in login. Please check your credentials.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    # if user.is_authenticated:
    logout(request)
    return redirect("login")


def custom_404(request, exception):
    return render(request, "account/custom404.html", {}, status=404)


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages


from django.contrib.auth.decorators import login_required


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to maintain the user's login status
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("login")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})
