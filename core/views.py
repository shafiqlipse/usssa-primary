from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from .models import *


# Create your views here.
def home(request):
    context = {}
    return render(request, "core/home.html", context)


def district(request):
    context = {}
    return render(request, "", context)


def Officera(request):

    if request.method == "POST":
        form = OfficerForm(request.POST, request.FILES)

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
        form = OfficerForm()

    context = {"form": form}
    return render(request, "school/newofficial.html", context)


def officers(request):
    officers = Officer.objects.all()
    context = {"officers": officers}
    return render(request, "school/officers.html", context)


def district(request):
    officer = request.user
    if officer.is_district:
        location = get_object_or_404(District, id=officer.district_id)
        schools = School.objects.filter(district=location)

    else:
        location = get_object_or_404(City, id=officer.city_id)
        schools = School.objects.filter(city=location)

    athletes = Athlete.objects.filter(school__in=schools)
    context = {"location": location, "schools": schools, "athletes": athletes}
    return render(request, "district_template.html", context)


from django.http import JsonResponse
from django.contrib import messages

from django.http import JsonResponse


def get_athletes(request):
    # Get the school associated with the logged-in user
    user = request.user
    officer = user.officer
    district = officer.district

    # Get all schools within the district
    schools = district.school_set.all()

    sport_id = request.GET.get("team_sport_id")
    gender = request.GET.get("team_gender")

    # Start with the base queryset for athletes in schools within the district
    athletes = Athlete.objects.filter(school__in=schools)

    # Apply additional filters for sport, gender, and age if provided
    if sport_id:
        athletes = athletes.filter(sport=sport_id)
    if gender:
        athletes = athletes.filter(gender=gender)

    # Retrieve only the necessary fields
    athletes = athletes.values("id", "name")

    # Wrap the athletes array in a JSON object with an 'athletes' property
    data = {"athletes": list(athletes)}

    return JsonResponse(data)


from django.views import View


def create_team(request):
    errors = None
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.team_officer = request.user
            team.save()
            return redirect("teams")
        else:
            # Attach errors to the form for display in the template
            errors = form.errors
    else:
        form = TeamForm()

    return render(request, "school/teamnew.html", {"form": form, "errors": errors})


# @school_required
def update_team(request, id):
    team = get_object_or_404(Team, pk=id)

    if request.method == "POST":
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            # Get selected athletes from the form
            athletes = form.cleaned_data.get("athletes")
            print("Athletes:", athletes)  # Debugging

            # Associate selected athletes with the team
            team.athletes.set(athletes)
            print("Team athletes:", team.athletes.all())  # Debugging
            return redirect("teams")  # Redirect to the team list page or another URL
    else:
        form = TeamForm(instance=team)

    return render(request, "teams/newteam.html", {"form": form, "team": team})


# from competitions.models import Fixture


def team_details(request, id):
    team = Team.objects.get(id=id)

    context = {"team": team}
    return render(request, "teams/team.html", context)


# # delete team


def delete_team(request, id):
    team = get_object_or_404(Team, pk=id)

    if request.method == "POST":
        team.delete()
        return redirect("teams")  # Redirect to the team list page or another URL

    return render(request, "school/delete_team.html", {"team": team})


def Teams(request):
    teams = Team.objects.all()
    context = {"teams": teams}
    return render(request, "school/teams.html", context)
