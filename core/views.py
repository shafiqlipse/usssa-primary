from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib import messages
from accounts.decorators import anonymous_required, admin_required, staff_required
from .models import *


# Create your views here.
def home(request):
    context = {}
    return render(request, "core/home.html", context)


@admin_required
def profile_update(request, id):
    officer = get_object_or_404(Officer, id=id)

    if request.method == "POST":
        form = OfficerForm(request.POST, instance=officer)
        if form.is_valid():
            form.save()
            return redirect("officer_dashboard")
    else:
        form = OfficerForm(instance=officer)

    context = {"form": form, "officer": officer}
    return render(request, "accounts/editprofile.html", context)


def Officera(request):

    if request.method == "POST":
        form = OfficerForm(request.POST, request.FILES)

        if form.is_valid():
            # admin_user = User.objects.get_or_create(username="admin")
            # Assign the currently logged-in user
            form.save()
            messages.success(request, "Account completed successfully!")
            return redirect("offcom")

        else:
            # Add form-specific error messages for individual fields
            messages.error(request, "Form is not valid. Please check your input.")
            print(f"Form errors: {form.errors}")

    else:
        form = OfficerForm()

    context = {"form": form}
    return render(request, "school/newofficial.html", context)


def newTofficer(request):

    if request.method == "POST":
        form = TOfficerForm(request.POST, request.FILES)

        if form.is_valid():

            # Assign the currently logged-in user
            tform = form.save(commit=False)
            tform.user = request.user
            tform.save()
            # messages.success(request, "Account completed successfully!")
            return redirect("tofficers")

        else:
            # errors = form.errors
            # pass
            # Add form-specific error messages for individual fields
            messages.error(request, "Form is not valid. Please check your input.")

    else:
        form = TOfficerForm()

    context = {"form": form}
    return render(request, "school/tofficer.html", context)


def officers(request):
    officers = Officer.objects.all()
    context = {"officers": officers}
    return render(request, "school/officers.html", context)


def Dofficers(request):
    tofficers = TOfficer.objects.all()
    context = {"tofficers": tofficers}
    return render(request, "school/tofficers.html", context)


def tofficers(request):
    tofficers = TOfficer.objects.filter(user=request.user)
    context = {"tofficers": tofficers}
    return render(request, "school/tofficers.html", context)


def tofficer_details(request, id):
    tofficer = TOfficer.objects.get(id=id)

    context = {"tofficer": tofficer}
    return render(request, "school/tofficera.html", context)


def officer_details(request, id):
    officer = Officer.objects.get(id=id)

    context = {"officer": officer}
    return render(request, "school/officer.html", context)


# # delete team


def delete_officer(request, id):
    officer = get_object_or_404(Officer, id=id)

    if request.method == "POST":
        officer.delete()
        return redirect("officers")  # Redirect to the team list page or another URL

    return render(request, "school/delete_team.html", {"officer": officer})


def AllTeams(request):
    teams = Team.objects.filter(team_officer=request.user)
    officer = Officer.objects.get(user=request.user)
    location = officer.district
    context = {"teams": teams, "location": location}
    return render(request, "school/teams.html", context)


@staff_required
def Teams(request):
    teams = Team.objects.all()
    context = {"teams": teams}
    return render(request, "school/teams.html", context)


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


from django.views import View


def create_team(request):
    errors = None
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.team_officer = request.user
            team.save()
            athletes = form.cleaned_data.get(
                "athletes"
            )  # Replace 'athletes' with the actual form field name
            team.athletes.set(athletes)
            team.save()
            return redirect("allteams")
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
        return redirect("allteams")  # Redirect to the team list page or another URL

    return render(request, "school/delete_team.html", {"team": team})


def Teams(request):
    teams = Team.objects.all()

    context = {"teams": teams}
    return render(request, "school/teams.html", context)


from django.shortcuts import render
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib.staticfiles import finders
import base64
import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from PIL import Image
from io import BytesIO


def compress_image(image_data, quality=85):
    img = Image.open(BytesIO(image_data))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    output = BytesIO()
    img.save(output, format="JPEG", quality=quality)
    compressed_image_data = output.getvalue()
    return compressed_image_data


def generate_dalbum(request, id):

    team = Team.objects.get(id=id)
    athletes = team.athletes.all()
    user = team.team_officer
    profile = user.officer_profile.first()
    district = profile.district
    # Get template
    template = get_template("school/Albums.html")

    # Compress school photo

    # Compress athletes' photos
    # for athlete in athletes:
    #     if athlete.photo:
    #         with default_storage.open(athlete.photo.path, "rb") as image_file:
    #             athlete_photo_data = image_file.read()
    #         compressed_athlete_photo_data = compress_image(athlete_photo_data)
    #         athlete.photo_base64 = base64.b64encode(
    #             compressed_athlete_photo_data
    #         ).decode("utf-8")

    # Prepare context
    context = {
        "team": team,
        "district": district,
        "athletes": athletes,
        "MEDIA_URL": settings.MEDIA_URL,
    }

    # Render HTML
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="District Album.pdf"'

    # Generate PDF from HTML
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    return response


def accreditation(request, id):

    team = Team.objects.get(id=id)
    athletes = team.athletes.all()
    district = team.team_officer.user.first().district
    # Get template
    template = get_template("school/accred.html")

    # Compress school photo

    # Compress athletes' photos
    for athlete in athletes:
        if athlete.photo:
            with default_storage.open(athlete.photo.path, "rb") as image_file:
                athlete_photo_data = image_file.read()
            compressed_athlete_photo_data = compress_image(athlete_photo_data)
            athlete.photo_base64 = base64.b64encode(
                compressed_athlete_photo_data
            ).decode("utf-8")

    # Prepare context
    context = {
        "district": district,
        "athletes": athletes,
        "MEDIA_URL": settings.MEDIA_URL,
    }

    # Render HTML
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Accreditation.pdf"'

    # Generate PDF from HTML
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    return response


def cert(request, id):

    team = Team.objects.get(id=id)
    athletes = team.athletes.all()

    # Get template
    template = get_template("school/cert.html")

    # Compress school photo

    # Compress athletes' photos
    for athlete in athletes:
        if athlete.photo:
            with default_storage.open(athlete.photo.path, "rb") as image_file:
                athlete_photo_data = image_file.read()
            compressed_athlete_photo_data = compress_image(athlete_photo_data)
            athlete.photo_base64 = base64.b64encode(
                compressed_athlete_photo_data
            ).decode("utf-8")

    # Prepare context
    context = {
        "athletes": athletes,
        "MEDIA_URL": settings.MEDIA_URL,
    }

    # Render HTML
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Certificate.pdf"'

    # Generate PDF from HTML
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    return response


def get_dist_athletes(request):
    # Get the officer associated with the logged-in user
    try:
        officer = Officer.objects.get(user=request.user)
        location = officer.district
    except Officer.DoesNotExist:
        return JsonResponse(
            {"error": "User is not associated with an officer"}, status=400
        )

    schools = School.objects.filter(district=location)

    team_gender = request.GET.get("team_gender")
    team_age = request.GET.get("team_age")  # Changed from age_id to team_age

    # Start with the base queryset for athletes in the user's schools
    athletes = Athlete.objects.filter(school__in=schools)

    # Apply additional filters for gender and age if provided
    if team_gender:
        athletes = athletes.filter(gender=team_gender)

    if team_age:
        athletes = athletes.filter(age=team_age)  # Assuming the field is named 'age'

    # Retrieve only the necessary fields
    athletes = athletes.values("id", "fname", "lname", "lin")

    # Wrap the athletes array in a JSON object with an 'athletes' property
    data = {"athletes": list(athletes)}

    return JsonResponse(data)


def taccreditation(request, id):

    officer = Officer.objects.get(id=id)
    tofficers = TOfficer.objects.filter(user_id=officer.user_id)
    # Get template
    template = get_template("school/taccred.html")

    # Compress school photo

    # Compress athletes' photos
    for tofficer in tofficers:
        if tofficer.photo:
            with default_storage.open(tofficer.photo.path, "rb") as image_file:
                athlete_photo_data = image_file.read()
            compressed_athlete_photo_data = compress_image(athlete_photo_data)
            tofficer.photo_base64 = base64.b64encode(
                compressed_athlete_photo_data
            ).decode("utf-8")

    # Prepare context
    context = {
        "officer": officer,
        "tofficers": tofficers,
        "MEDIA_URL": settings.MEDIA_URL,
    }

    # Render HTML
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="OfficerAccreditation.pdf"'

    # Generate PDF from HTML
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    return response


def delloff(request, id):
    stud = TOfficer.objects.get(id=id)
    if request.method == "POST":
        stud.delete()
        return redirect("tofficers")

    return render(request, "dashboard/deleteath.html", {"obj": stud})
