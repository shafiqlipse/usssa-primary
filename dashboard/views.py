from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import *
from accounts.forms import *
from .models import *
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
    schools = School.objects.all()
    schools_count = School.objects.all().count
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
        "schools_count": schools_count,
        "athletes_bcount": athletes_bcount,
        "athletes_gcount": athletes_gcount,
        "officials_count": officials_count,
        "officials_bcount": officials_bcount,
        "officials_gcount": officials_gcount,
    }
    return render(request, "dashboard/overview.html", context)



# schools


# schools list, tuple or array
@staff_required
def schools(request):

    schools = School.objects.all()

    myFilter = schoolsFilter(request.GET, queryset=schools)

    schoollist = myFilter.qs

    items_per_page = 10

    paginator = Paginator(schoollist, items_per_page)
    page = request.GET.get("page")

    try:
        schoollist = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page
        schoollist = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page
        schoollist = paginator.page(paginator.num_pages)
    context = {
        "schoollist": schoollist,
        # "teamsFilter": teamsFilter,
        "myFilter": myFilter,
        # "teamlist": teamlist,
        "schools": schools,
    }
    return render(request, "dashboard/schools.html", context)


# schools list, tuple or array
@staff_required
def all_athletes(request):

    athletes = Athlete.objects.all()

    myFilter = AthletesFilter(request.GET, queryset=athletes)

    athletelist = myFilter.qs

    items_per_page = 10

    paginator = Paginator(athletelist, items_per_page)
    page = request.GET.get("page")

    try:
        athletelist = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page
        athletelist = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page
        athletelist = paginator.page(paginator.num_pages)
    context = {
        "athletelist": athletelist,
        # "teamsFilter": teamsFilter,
        "myFilter": myFilter,
        # "teamlist": teamlist,
        "athletes": athletes,
    }
    return render(request, "dashboard/athletes.html", context)


# Import the traceback module for logging


@staff_required
def Schoolnew(request):
    regions = Region.objects.all()

    if request.method == "POST":
        form = SchoolProfileForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                schoolX = form.save(commit=False)
                schoolX.user = request.user  # Assign the currently logged-in user
                schoolX.save()
                messages.success(request, "Account completed successfully!")
                return redirect("dashboard")

            except Exception as e:
                # Log the exception for debugging
                traceback.print_exc()

                # Add a form-specific error message
                form.add_error(None, f"Error adding school: {str(e)}")
                messages.error(
                    request,
                    "There was an error with the form submission. Please try again.",
                )
                print(f"Error adding school: {str(e)}")
        else:
            # Add form-specific error messages for individual fields
            messages.error(request, "Form is not valid. Please check your input.")
            print(f"Form errors: {form.errors}")

    else:
        form = SchoolProfileForm()

    context = {"form": form, "regions": regions}
    return render(request, "school/create_school.html", context)


@staff_required
def school_detail(request, id):
    school = School.objects.get(id=id)
    officials = school_official.objects.filter(school_id=id)
    off = school_official.objects.filter(school_id=id).count
    athletes = Athlete.objects.filter(school_id=id)
    ath = Athlete.objects.filter(school_id=id).count
    new_official = None

    # new_comment_reply = None

    if request.method == "POST":
        cform = OfficialForm(request.POST, request.FILES)

        if cform.is_valid():
            new_official = cform.save(commit=False)
            new_official.school = school
            new_official.save()
            return redirect("schooldetail", id)
    else:
        cform = OfficialForm()

    myFilter = OfficialFilter(request.GET, queryset=officials)

    officialist = myFilter.qs

    items_per_page = 10

    paginator = Paginator(officialist, items_per_page)
    page = request.GET.get("page")

    try:
        officialist = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page
        officialist = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page
        officialist = paginator.page(paginator.num_pages)

    myAFilter = AthleteFilter(request.GET, queryset=athletes)

    athletelist = myAFilter.qs

    items_per_page = 10

    paginator = Paginator(athletelist, items_per_page)
    page = request.GET.get("page")

    try:
        athletelist = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page
        athletelist = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page
        athletelist = paginator.page(paginator.num_pages)
    context = {
        "officialist": officialist,
        "athletelist": athletelist,
        # "teamsFilter": teamsFilter,
        "myFilter": myFilter,
        "myAFilter": myAFilter,
        # "teamlist": teamlist,
        "schools": schools,
        "school": school,
        "cform": cform,
        "ath": ath,
        "off": off,
    }
    return render(request, "school/school.html", context)


# schools list, tuple or array
def Tournaments(request):

    # schools = school.objects.all()

    # # schoolFilter = schoolFilter(request.GET, queryset=schools)
    # myFilter = schoolFilter(request.GET, queryset=schools)

    # schoollist = myFilter.qs

    # items_per_page = 10

    # paginator = Paginator(schoollist, items_per_page)
    # page = request.GET.get("page")

    # try:
    #     schoollist = paginator.page(page)
    # except PageNotAnInteger:
    #     # If the page is not an integer, deliver the first page
    #     schoollist = paginator.page(1)
    # except EmptyPage:
    #     # If the page is out of range, deliver the last page
    #     schoollist = paginator.page(paginator.num_pages)
    context = {
        #     "schoollist": schoollist,
        #     # "teamsFilter": teamsFilter,
        #     "myFilter": myFilter,
        #     # "teamlist": teamlist,
    }
    return render(request, "dashboard/tournaments.html", context)


# schools list, tuple or array
def districts(request):

    # schools = school.objects.all()

    # # schoolFilter = schoolFilter(request.GET, queryset=schools)
    # myFilter = schoolFilter(request.GET, queryset=schools)

    # schoollist = myFilter.qs

    # items_per_page = 10

    # paginator = Paginator(schoollist, items_per_page)
    # page = request.GET.get("page")

    # try:
    #     schoollist = paginator.page(page)
    # except PageNotAnInteger:
    #     # If the page is not an integer, deliver the first page
    #     schoollist = paginator.page(1)
    # except EmptyPage:
    #     # If the page is out of range, deliver the last page
    #     schoollist = paginator.page(paginator.num_pages)
    context = {
        #     "schoollist": schoollist,
        #     # "teamsFilter": teamsFilter,
        #     "myFilter": myFilter,
        #     # "teamlist": teamlist,
    }
    return render(request, "dashboard/districts.html", context)


# schools list, tuple or array
def zones(request):

    # schools = school.objects.all()

    # # schoolFilter = schoolFilter(request.GET, queryset=schools)
    # myFilter = schoolFilter(request.GET, queryset=schools)

    # schoollist = myFilter.qs

    # items_per_page = 10

    # paginator = Paginator(schoollist, items_per_page)
    # page = request.GET.get("page")

    # try:
    #     schoollist = paginator.page(page)
    # except PageNotAnInteger:
    #     # If the page is not an integer, deliver the first page
    #     schoollist = paginator.page(1)
    # except EmptyPage:
    #     # If the page is out of range, deliver the last page
    #     schoollist = paginator.page(paginator.num_pages)
    context = {
        #     "schoollist": schoollist,
        #     # "teamsFilter": teamsFilter,
        #     "myFilter": myFilter,
        #     # "teamlist": teamlist,
    }
    return render(request, "dashboard/zones.html", context)


@school_required
def Dash(request):
    user = request.user
    school = School.objects.get(user_id=user.id)
    officials_count = school_official.objects.filter(school_id=school.id).count
    officials = school_official.objects.filter(school_id=school.id)
    context = {
        "officials_count": officials_count,
        "officials": officials,
        "school": school,
    }
    return render(request, "school/schoolprofile.html", context)


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
    myFilter = AthleteFilter(request.GET, queryset=athletes)

    athletelist = myFilter.qs

    items_per_page = 10

    paginator = Paginator(athletelist, items_per_page)
    page = request.GET.get("page")

    try:
        athletelist = paginator.page(page)
    except PageNotAnInteger:
        # If the page is not an integer, deliver the first page
        athletelist = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page
        athletelist = paginator.page(paginator.num_pages)
    context = {
        "athletelist": athletelist,
        # "teamsFilter": teamsFilter,
        "myFilter": myFilter,
        # "teamlist": teamlist,
    }

    return render(request, "school/athletes.html", context)


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
