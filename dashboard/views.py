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
    }
    return render(request, "dashboard/overview.html", context)


# schools


# schools list, tuple or array
@staff_required
def users(request):

    users = User.objects.all()

    context = {
        "users": users,
        # "teamsFilter": teams
    }
    return render(request, "dashboard/users.html", context)


# schools list, tuple or array
#@staff_required
def schools(request):

    schools = School.objects.all()

    context = {
        "schools": schools,
        # "teamsFilter": teams
    }
    return render(request, "dashboard/schools.html", context)


# schools list, tuple or array
@staff_required
def activeschools(request):

    schools = School.objects.filter(status="Active")

    context = {
        "schools": schools,
        # "teamsFilter": teams
    }
    return render(request, "dashboard/active.html", context)


# schools list, tuple or array
@staff_required
def inactiveschools(request):

    schools = School.objects.filter(status="Inactive")

    context = {
        "schools": schools,
        # "teamsFilter": teams
    }
    return render(request, "dashboard/inactive.html", context)


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
    return render(request, "dashboard/athletes.html", context)


# schools list, tuple or array
@staff_required
def all_officials(request):

    officilas = school_official.objects.all()

    context = {
        "officilas": officilas,
    }
    return render(request, "dashboard/officials.html", context)


def Schoolnew(request):
    regions = Region.objects.all()

    if request.method == "POST":
        form = SchoolProfileForm(request.POST, request.FILES)

        if form.is_valid():
            # admin_user = User.objects.get_or_create(username="admin")
            # Assign the currently logged-in user
            form.save()
            messages.success(request, "Account completed successfully!")
            return redirect("confirmation")

        else:
            # Add form-specific error messages for individual fields
            messages.error(request, "Form is not valid. Please check your input.")
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
    return render(request, "school/NOfficial.html", context)


# schools list, tuple or array
def Tournaments(request):

    tournaments = Tournament.objects.all()

    context = {"tournaments": tournaments}
    return render(request, "dashboard/tournaments.html", context)


# schools list, tuple or array
def districts(request):

    districts = District.objects.all()

    # schoolFilter = schoolFilter(request.GET, queryset=schools)
    myFilter = districtsFilter(request.GET, queryset=districts)

    districtslist = myFilter.qs

    items_per_page = 10

    paginator = Paginator(districtslist, items_per_page)
    page = request.GET.get("page")

    try:
        districtslist = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page
        districtslist = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page
        districtslist = paginator.page(paginator.num_pages)

    context = {
        "districtslist": districtslist,
        "myFilter": myFilter,
    }
    return render(request, "dashboard/districts.html", context)


# schools list, tuple or array
def municipalities(request):

    municipalities = Municipality.objects.all()

    context = {
        "municipalities": municipalities,
    }
    return render(request, "dashboard/zones.html", context)


@school_required
def Dash(request):
    user = request.user
    school = School.objects.get(user_id=user.id)
    officials_count = school_official.objects.filter(school_id=school.id).count()
    athletes_count = Athlete.objects.filter(school_id=school.id).count()
    officials_bcount = school_official.objects.filter(
        school_id=school.id, gender="M"
    ).count()
    officials_gcount = school_official.objects.filter(
        school_id=school.id, gender="F"
    ).count()
    athletes_gcount = Athlete.objects.filter(
        school_id=school.id, gender="Female"
    ).count()
    athletes_bcount = Athlete.objects.filter(school_id=school.id, gender="Male").count()
    officials = school_official.objects.filter(school_id=school.id)
    context = {
        "officials_count": officials_count,
        "officials_bcount": officials_bcount,
        "officials_gcount": officials_gcount,
        "athletes_count": athletes_count,
        "athletes_bcount": athletes_bcount,
        "athletes_gcount": athletes_gcount,
        "officials": officials,
        "school": school,
    }
    return render(request, "school/schoolprofile.html", context)


# @school_required
def Officerdash(request):
    user = request.user
    officer = Officer.objects.get(user_id=user.id)
    district = officer.district
    schools = School.objects.filter(district=district)
    athletes = Athlete.objects.filter(school__in=schools)
    schools_cout = School.objects.filter(district=district).count()
    athletes_count = Athlete.objects.filter(school__in=schools).count()

    context = {
        "officer": officer,
        "district": district,
        "schools": schools,
        "schools_cout": schools_cout,
        "athletes": athletes,
        "athletes_count": athletes_count,
    }
    return render(request, "accounts/dprofile.html", context)


@login_required
def newAthlete(request):
    if request.method == "POST":
        form = NewAthleteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_athlete = form.save(commit=False)
                new_athlete.school = request.user.school_profile.first()
                new_athlete.save()
                messages.success(request, "Athlete added successfully!")
                return redirect("athletes")
            except Exception as e:
                messages.error(request, f"Error adding athlete: {str(e)}")
        else:
            messages.error(request, "Form is not valid. Please check your input.")
    else:
        form = NewAthleteForm()

    return render(request, "school/newAthlete.html", {"form": form})


# a confirmation of credentials
# @login_required
def confirmation(request):
    user = request.user
    context = {"user": user}
    return render(request, "confirm.html", context)


def offcom(request):
    user = request.user
    context = {"user": user}
    return render(request, "offcom.html", context)


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
def AthleteDetail(request, id):
    athlete = get_object_or_404(Athlete, id=id)
    relatedathletes = Athlete.objects.filter(school=athlete.school).exclude(id=id)

    context = {
        "athlete": athlete,
        "relatedathletes": relatedathletes,
        # "breadcrumbs": breadcrumbs,
    }

    return render(request, "school/athlete.html", context)


# @login_required(login_url="login")
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

    return render(request, "school/athletes.html", context)


# @login_required(login_url="login")
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

    return render(request, "school/officials.html", context)


@staff_required
def AthleteUpdate(request, id):
    band = Athlete.objects.get(id=id)

    if request.method == "POST":
        form = NewAthleteForm(request.POST, instance=band)
        if form.is_valid():
            form.save()

            return redirect("athletes")
    else:
        form = NewAthleteForm(instance=band)
    context = {"form": form}
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

    return render(request, "school/official.html", context)


def athlete_list(request):
    athletes = Athlete.objects.all()
    form = AthleteSelectionForm()

    if request.method == "POST":
        form = AthleteSelectionForm(request.POST)
        if form.is_valid():
            selected_athletes = form.cleaned_data["athletes"]
            total_amount = 1500 * len(selected_athletes)

            # Update the payment total_amount
            payment, created = Payment.objects.get_or_create(is_paid=False)
            payment.total_amount += total_amount
            payment.save()

            # Add selected athletes to the payment without deleting them
            payment.athletes.add(*selected_athletes)

            # Mark selected athletes as paid
            Athlete.objects.filter(
                pk__in=[athlete.pk for athlete in selected_athletes]
            ).update(is_paid=True)

            return redirect("payment_page")

    context = {"athletes": athletes, "form": form}
    return render(request, "school/athlete_list.html", context)


def payment_page(request):
    payment = Payment.objects.filter(is_paid=False).first()
    context = {"payment": payment}
    return render(request, "school/payment_page.html", context)


import requests
from django.conf import settings


def initiate_payment(request):
    # Retrieve Airtel Money credentials from settings
    client_id = settings.AIRTEL_MONEY_CLIENT_ID
    client_secret = settings.AIRTEL_MONEY_CLIENT_SECRET

    # Your payment initiation logic here
    # Make requests to Airtel Money API using client_id, client_secret, etc.
    # Example:
    response = requests.post(
        "https://openapiuat.airtel.africa/",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
        },
    )

    # Process the response and handle accordingly
    # Example:
    if response.status_code == 200:
        return HttpResponse("Payment initiated successfully")
    else:
        return HttpResponse("Failed to initiate payment")
