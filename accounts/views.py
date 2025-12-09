from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from accounts.decorators import anonymous_required, staff_required
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib import messages
# from .forms import SchoolRegistrationForm
# from dashboard.models import school_official, School, Athlete
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# Create your views here.
@anonymous_required  # Ensure this is properly defined
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            logout(request)  # Prevent session fixation
            login(request, user)

            if getattr(user, 'is_school', False):
                messages.success(request, "School login successful.")
                return redirect("school_dashboard")
            elif getattr(user, 'is_admin', False):
                messages.success(request, "Officer login successful.")
                return redirect("officer_dashboard")
            else:
                messages.success(request, "Login successful.")
                return redirect("dashboard")
        else:
            messages.error(request, f"Error in login: {form.errors}")
    else:
        form = AuthenticationForm()

    return render(request, "auth/login.html", {"form": form})
def user_logout(request):
    # if user.is_authenticated:
    logout(request)
    return redirect("login")


def custom_404(request, exception):
    return render(request, "account/custom404.html", {}, status=404)


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
    return render(request, "passwords/change_password.html", {"form": form})


# reportlab pdf generation of reports certificates and albums
from django.shortcuts import get_object_or_404
from.forms import UserEditForm

@login_required
def edit_user(request, id=None):
    if id:
        # Fetch the user to edit by their ID
        user = get_object_or_404(User, id=id)
    else:
        # Default to the logged-in user if no ID is provided
        user = request.user

    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "The profile was updated successfully.")
            return redirect("users")
    else:
        form = UserEditForm(instance=user)

    return render(request, "accounts/edit_user.html", {"form": form, "id": user.id})



# views.py
# import requests
# from django.shortcuts import render, redirect
# from .models import Payment

# schools list, tuple or array
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import User
from django.db.models import Q
def users_data(request):
    """ Handle AJAX DataTables request for large datasets """

    try:
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get("search[value]", "")

        # Fetch and filter users
        users_query = User.objects.filter(is_school=True)

        # Apply search across multiple fields
        if search_value:
            users_query = users_query.filter(
                Q(username__icontains=search_value) |
                Q(email__icontains=search_value) |
                Q(school_profile__school_name__icontains=search_value) |  # Search school name
                Q(school_profile__EMIS__icontains=search_value)   # Search EMIS
            )

        # Paginate results
        paginator = Paginator(users_query, length)
        page_number = (start // length) + 1
        users_page = paginator.get_page(page_number)

        # Prepare JSON response
        data = []
        for user in users_page:
            school = user.school_profile.first() if user.school_profile.exists() else None
            school_name = school.school_name if school else "No School"
            emis = school.EMIS if school else "N/A"

            action_buttons = f"""
                
                <a href="/dashboard/user/edit/{user.id}/" class="btn btn-warning btn-sm">Edit</a>
                
            """

            data.append({
                "username": user.username,
                "email": user.email,
                "school_profile": f"{school_name} | {emis}",
                "actions": action_buttons,
            })

        response = {
            "draw": draw,
            "recordsTotal": User.objects.filter(is_school=True).count(),
            "recordsFiltered": users_query.count(),
            "data": data,
        }

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

# def initiate_payment(request):
#     if request.method == 'POST':
#         amount = request.POST.get('amount')
#         description = request.POST.get('description')
#         phone_number = request.POST.get('phone_number')
@staff_required
def users(request):
    staff = User.objects.all().exclude(is_school=True)
    users = User.objects.select_related("school").filter(is_school=True)

    context = {
        "users": users,
        "staff": staff,
        # "teamsFilter": teams
    }
    return render(request, "accounts/users.html", context)

@staff_required
def staff(request):
    staff = User.objects.filter(is_staff=True)
    

    context = {
        "staff": staff,
        # "teamsFilter": teams
    }
    return render(request, "accounts/staff.html", context)

@staff_required
def sports_officers(request):
    sports_officers = User.objects.filter(is_admin=True)

    context = {
        "sports_officers": sports_officers,
    }
    return render(request, "accounts/sports.html", context)




from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "passwords/password_reset.html"
    email_template_name = "passwords/password_reset_email.html"
    subject_template_name = "passwords/password_reset_subject.txt"
    success_message = (
        "We've emailed you instructions for setting your password, "
        "if an account exists with the email you entered. You should receive them shortly."
        " If you don't receive an email, "
        "please make sure you've entered the address you registered with, and check your spam folder."
    )
    success_url = reverse_lazy("home")


