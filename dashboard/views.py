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
    anonymous_required,
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
# Create your views here.
def get_districts(request):
    region_id = request.GET.get("region_id")
    districts = District.objects.filter(region_id=region_id).values("id", "name")
    return JsonResponse(list(districts), safe=False)


# schools
# Create your views here.
def get_counties(request):
    district_id = request.GET.get("district_id")
    counties = County.objects.filter(district_id=district_id).values("id", "name")
    return JsonResponse(list(counties), safe=False)


# schools
# Create your views here.
def get_subcounties(request):
    county_id = request.GET.get("county_id")
    subcounties = Subcounty.objects.filter(county_id=county_id).values("id", "name")
    return JsonResponse(list(subcounties), safe=False)


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
    relatedathletes = school_official.objects.filter(school=official.school).exclude(id=id)

    context = {
        "official": official,
        "relatedathletes": relatedathletes,
        # "breadcrumbs": breadcrumbs,
    }

    return render(request, "school/official.html", context)
