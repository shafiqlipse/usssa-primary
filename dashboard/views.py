from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import *
from accounts.forms import *
from .models import *
from .forms import *
from accounts.forms import *
from django.utils import timezone

from .filters import *
from django.contrib import messages
from django.http import JsonResponse
from accounts.decorators import (
    school_required,
    staff_required,
    login_required,
)
import traceback



# Create your views here.
@staff_required
def Overview(request):
    # today = timezone.now().date()
    schools = School.objects.all()
    active_schools = School.objects.filter(status="Active").count
    inactive_schools = School.objects.filter(status="Inactive").count
    schools_count = School.objects.all().count
    # schools_today = School.objects.filter(created_at__date=today).count
    athletes = Athlete.objects.all()
    athletes_count = Athlete.objects.all().count
    officials_count = school_official.objects.all().count
    athletes_bcount = Athlete.objects.filter(gender="male").count
    athletes_gcount = Athlete.objects.filter(gender="female").count
    officials_bcount = school_official.objects.filter(gender="M").count
    officials_gcount = school_official.objects.filter(gender="F").count
    # greeting = get_greeting()
    context = {
        "athletes": athletes,
        "schools": schools,
        "athletes_count": athletes_count,
        # "schools_today": schools_today,
        "schools_count": schools_count,
        "athletes_bcount": athletes_bcount,
        "athletes_gcount": athletes_gcount,
        "officials_count": officials_count,
        "officials_bcount": officials_bcount,
        "officials_gcount": officials_gcount,
        "active_schools": active_schools,
        "inactive_schools": inactive_schools,
        # "greeting": greeting,
    }
    return render(request, "dashboard/analytics.html", context)


# schools


# schools list, tuple or array
# @staff_required
# def users(request):

#     users = User.objects.all()

#     context = {
#         "users": users,
#         # "teamsFilter": teams
#     }
#     return render(request, "dashboard/users.html", context)


# schools list, tuple or array
# @staff_required
def schools(request):

    schools = School.objects.all()

    context = {
        "schools": schools,
        # "teamsFilter": teams
    }
    return render(request, "school/schools.html", context)





# hegfhjgfjdhfjhfjdjjjjjjjjjjjjjjjjjjjjjjjj

import csv
from django.http import HttpResponse
from .models import School
from core.models import *


def export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="schools.csv"'

    writer = csv.writer(response)
    writer.writerow(["School Name", "EMIS", "Contact", "District"])  # CSV header

    # Fetch data from the database and write it to the CSV file
    schools = School.objects.all()
    for school in schools:
        writer.writerow(
            [school.school_name, school.EMIS, school.phone_number, school.district]
        )

    return response


def exportp_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="schools.csv"'

    writer = csv.writer(response)
    writer.writerow(["School Name", "EMIS", "Contact", "District"])  # CSV header

    # Fetch data from the database and write it to the CSV file
    schools = School.objects.filter(status="Active")
    for school in schools:
        writer.writerow(
            [school.school_name, school.EMIS, school.phone_number, school.district]
        )

    return response


# schools list, tuple or array
# schools list, tuple or array
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from .models import School
# from teams.models import SchoolTeam
from django.db import IntegrityError
from django.db import IntegrityError
from django.core.files.base import ContentFile
import base64


def export_pdf(request):
    # Create a response object with PDF content type
    response = HttpResponse(content_type="application/pdf")
    # Set the content disposition to force download
    response["Content-Disposition"] = 'attachment; filename="schools.pdf"'

    # Fetch data from the database
    schools = School.objects.all()

    # Create a list to hold the data for the table
    data = [
        ["#", "School Name", "EMIS", "Contact", "District"]
    ]  # Added "#" for numbering

    # Populate the data list with school details
    for idx, school in enumerate(schools, start=1):
        data.append(
            [
                idx,
                school.school_name,
                school.EMIS,
                school.phone_number,
                school.district if school.district else "N/A",
            ]
        )

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)
    # Create a table with the school data
    table = Table(data)

    # Add style to the table
    style = TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkred),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ("BACKGROUND", (0, 1), (-1, -1), colors.white),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ]
    )

    # Set column widths
    table_width = doc.width
    col_widths = [table_width * 1] + [table_width * 1] * (
        len(data[0]) - 1
    )  # Adjusted the column widths
    table.setStyle(TableStyle([("WIDTH", (1, 1), (0, 0), col_widths)]))

    table.setStyle(style)
    # Add the table to the PDF document
    doc.build([table])

    return response


# schools list, tuple or array
@staff_required
def all_athletes(request):

    athletes = Athlete.objects.all()

    context = {
        "athletes": athletes,
    }
    return render(request, "athletes/athletes.html", context)


# schools list, tuple or array
@staff_required
def all_officials(request):

    officilas = school_official.objects.all()

    context = {
        "officilas": officilas,
    }
    return render(request, "officials/officials.html", context)


def Schoolnew(request):
    regions = Region.objects.all()

    if request.method == "POST":
        form = SchoolProfileForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Account completed successfully!")
                return redirect("confirmation")
            except IntegrityError as e:
                if "EMIS" in str(e):
                    messages.error(
                        request, "A school with this EMIS number already exists."
                    )
                else:
                    messages.error(
                        request,
                        "An error occurred while saving the school. Please fill all required fields.",
                    )
        else:
            # Add more detailed error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            print(f"Form errors: {form.errors}")

    else:
        form = SchoolProfileForm()

    context = {"form": form, "regions": regions}
    return render(request, "school/create_school.html", context)


@staff_required
def school_update(request, id):
    school = get_object_or_404(School, id=id)

    if request.method == "POST":
        form = SchoolEditForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            return redirect("schools")
    else:
        form = SchoolEditForm(instance=school)

    context = {"form": form, "school": school}
    return render(request, "dashboard/editschool.html", context)


@login_required
def schoolupdate(request, id):
    school = School.objects.get(id=id)

    if request.method == "POST":
        form = SchoolProfileForm(request.POST, instance=school)
        if form.is_valid():
            form.save()

            return redirect("school_dashboard")
    else:
        form = SchoolProfileForm(instance=school)
    context = {"form": form}
    return render(request, "school/create_school.html", context)


# @staff_required
@login_required
def school_detail(request, id):
    school = get_object_or_404(School, id=id)
    officials = school_official.objects.filter(school_id=id)
    athletes = Athlete.objects.filter(school_id=id)

    context = {
        "school": school,
        "athletes": athletes,
        "officials": officials,
    }
    return render(request, "school/school.html", context)


# schools list, tuple or array
@school_required
def Official(request):
    if request.method == "POST":
        form = OfficialForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                official = form.save(commit=False)
                official.school = request.user.school_profile.first()
                official.save()
                messages.success(request, "Official added successfully!")
                return redirect("officials")
            except Exception as e:
                messages.error(request, f"Error adding athlete: {str(e)}")
        else:
            messages.error(request, "Form is not valid. Please check your input.")
    else:
        form = OfficialForm()

    context = {"form": form}
    return render(request, "officials/NOfficial.html", context)


# schools list, tuple or array
def Tournaments(request):

    tournaments = Tournament.objects.all()

    context = {"tournaments": tournaments}
    return render(request, "dashboard/tournaments.html", context)



def Dash(request):
    user = request.user
    school = School.objects.get(user_id=user.id)
    officials_count = school_official.objects.filter(school_id=school.id).count()
    athletes_count = Athlete.objects.filter(school_id=school.id).count()
    athletes = Athlete.objects.filter(school_id=school.id)[:6]
    officials_bcount = school_official.objects.filter(
        school_id=school.id, gender="M"
    ).count()
    officials_gcount = school_official.objects.filter(
        school_id=school.id, gender="F"
    ).count()
    athletes_gcount = Athlete.objects.filter(
        school_id=school.id, gender="Female"
    ).count()
    # teams_gcount = SchoolTeam.objects.filter(
    #     school_id=school.id, gender="Female"
    # # ).count()
    # teams_bcount = SchoolTeam.objects.filter(
    #     school_id=school.id, gender="Male"
    # # ).count()
    athletes_bcount = Athlete.objects.filter(school_id=school.id, gender="Male").count()
    officials = school_official.objects.filter(school_id=school.id)
    # teams = SchoolTeam.objects.filter(school_id=school.id).count

    # from django.contrib.auth.hashers import make_password

    context = {
        "officials_count": officials_count,
        "officials_bcount": officials_bcount,
        "officials_gcount": officials_gcount,
        "athletes_count": athletes_count,
        "athletes_bcount": athletes_bcount,
        "athletes_gcount": athletes_gcount,
        "officials": officials,
        "school": school,
        "athletes": athletes,
        # "teams": teams,
        # "teams_gcount": teams_gcount,
        # "teams_bcount": teams_bcount,
    }
    return render(request, "school/schoolprofile.html", context)


@login_required
def newAthlete(request):
    if request.method == "POST":
        form = NewAthleteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_athlete = form.save(commit=False)

                # Assign the school from the user profile
                new_athlete.school = (
                    request.user.school_profile.first()
                )  # Ensure profile has a school

                # Handle cropped image data for the "photo" field
                cropped_data = request.POST.get("photo_cropped")
                if cropped_data:
                    try:
                        format, imgstr = cropped_data.split(";base64,")
                        ext = format.split("/")[-1]
                        data = ContentFile(
                            base64.b64decode(imgstr), name=f"photo.{ext}"
                        )
                        new_athlete.photo = data  # Assign cropped image
                    except (ValueError, TypeError) as e:
                        messages.error(request, "Invalid image data.")
                        return render(
                            request, "athletes/newAthlete.html", {"form": form}
                        )

                new_athlete.save()
                messages.success(request, "Athlete added successfully!")
                return redirect("athletes")

            except IntegrityError as e:
                if "lin" in str(e).lower():
                    messages.error(
                        request,
                        "An athlete with this Learner Identification Number (LIN) already exists.",
                    )
                else:
                    messages.error(request, f"Error adding athlete: {str(e)}")
            except Exception as e:
                messages.error(request, f"Error adding athlete: {str(e)}")
        else:
            # Form validation error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        form = NewAthleteForm()

    return render(request, "athletes/newAthlete.html", {"form": form})



# @login_required
def confirmation(request):
    user = request.user
    context = {"user": user}
    return render(request, "confirm.html", context)


def offcom(request):
    user = request.user
    context = {"user": user}
    return render(request, "offcom.html", context)


def ofifcom(request):
    user = request.user
    context = {"user": user}
    return render(request, "ofifcom.html", context)


from django.http import JsonResponse
import datetime
from django.contrib import messages


def calculate_age_choices(request):
    date_of_birth_str = request.GET.get("date_of_birth")

    # Check if date_of_birth_str is None
    if date_of_birth_str is None:
        return JsonResponse({"error": "Date of birth is missing"}, status=400)

    # Convert date_of_birth string to a datetime.date object
    date_of_birth = datetime.datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()

    # Calculate the athlete's age based on the date of birth
    current_year = datetime.date.today().year
    calculated_age = (
        current_year
        - date_of_birth.year
        - (
            (datetime.date.today().month, datetime.date.today().day)
            < (date_of_birth.month, date_of_birth.day)
        )
    )

    # Filter the Age model to get age choices based on the calculated age
    age_choices = Age.objects.filter(
        min_age__lte=calculated_age, max_age__gte=calculated_age
    ).values_list("id", "name")

    # Prepare the JSON response
    response_data = {"ages": list(age_choices)}

    return JsonResponse(response_data)


# # Athletes details......................................................
@login_required
def AthleteDetail(request, id):
    athlete = get_object_or_404(Athlete, id=id)
    relatedathletes = Athlete.objects.filter(school=athlete.school).exclude(id=id)

    context = {
        "athlete": athlete,
        "relatedathletes": relatedathletes,
        # "breadcrumbs": breadcrumbs,
    }

    return render(request, "athletes/athlete.html", context)


@login_required(login_url="login")
def athletes(request):
    user = request.user
    school_profile = (
        user.school_profile.first()
    )  # Retrieve the first related School object
    if school_profile:
        school_id = school_profile.id
        athletes = Athlete.objects.filter(school_id=school_id)
    else:
        # Handle the case where the user is not associated with any school
        athletes = Athlete.objects.none()
    # officialFilter = OfficialFilter(request.GET, queryset=officials)

    context = {"athletes": athletes, "school_profile": school_profile}

    return render(request, "athletes/athletes.html", context)


@login_required(login_url="login")
def school_offs(request):
    user = request.user
    school_profile = (
        user.school_profile.first()
    )  # Retrieve the first related School object
    if school_profile:
        school_id = school_profile.id
        school_offs = school_official.objects.filter(school_id=school_id)
    else:
        # Handle the case where the user is not associated with any school
        school_offs = school_official.objects.none()
    # officialFilter = OfficialFilter(request.GET, queryset=officials)

    context = {
        "school_offs": school_offs,
    }

    return render(request, "officials/officials.html", context)


@login_required
def AthleteUpdate(request, id):
    athlete = get_object_or_404(Athlete, id=id)

    if request.method == "POST":
        form = NewAthleteForm(request.POST, request.FILES, instance=athlete)
        if form.is_valid():
            form.save()
            messages.success(request, "Athlete information updated successfully!")
            return redirect("athletes")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NewAthleteForm(instance=athlete)

    context = {
        "form": form,
        "athlete": athlete,
    }
    return render(request, "school/newAthlete.html", context)


# # Athletes details......................................................
# # Athletes details......................................................
@login_required(login_url="login")
def DeleteAthlete(request, id):
    stud = Athlete.objects.get(id=id)
    if request.method == "POST":
        stud.delete()
        return redirect("athletes")

    return render(request, "dashboard/deleteath.html", {"obj": stud})


# # Athletes details......................................................
@login_required(login_url="login")
def DeleteSchool(request, id):
    stud = School.objects.get(id=id)
    if request.method == "POST":
        stud.delete()
        return redirect("schools")

    return render(request, "dashboard/deletesch.html", {"obj": stud})


# # Athletes details......................................................
def OfficialDetail(request, id):
    official = get_object_or_404(school_official, id=id)
    relatedathletes = school_official.objects.filter(school=official.school).exclude(
        id=id
    )

    context = {
        "official": official,
        "relatedathletes": relatedathletes,
        # "breadcrumbs": breadcrumbs,
    }

    return render(request, "officials/official.html", context)


def athlete_list(request):
    athletes = Athlete.objects.all()

    context = {"athletes": athletes}
    return render(request, "school/athlete_list.html", context)


