from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import school_required, anonymous_required
from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.


@school_required
def get_athletes(request):
    # Get the school associated with the logged-in user
    school = get_object_or_404(School, user=request.user)
    school_id = school.id

    sport_id = request.GET.get("sport_id")
    gender = request.GET.get("gender")
    age_id = request.GET.get("age_id")

    # Start with the base queryset for athletes in the user's school
    athletes = Athlete.objects.filter(school_id=school_id)

    # Apply additional filters for sport, gender, and age if provided
    if sport_id:
        athletes = athletes.filter(sport_id=sport_id)

    if gender:
        athletes = athletes.filter(gender=gender)

    if age_id:
        athletes = athletes.filter(age_id=age_id)

    # Retrieve only the necessary fields
    athletes = athletes.values("id", "name")

    # Wrap the athletes array in a JSON object with an 'athletes' property
    data = {"athletes": list(athletes)}

    

    return JsonResponse(data)





def create_team(request):
    if request.method == "POST":
        form = SchoolTeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            # Assuming 'school' is the correct attribute name for the school in your Team model
            # Retrieve the school instance associated with the current user
            school_instance = get_object_or_404(School, user=request.user)
            # Assign the school instance to the team
            team.school = school_instance
            team.save()

            return redirect("team_s")
        else:
            # Attach errors to the form for display in the template
            error_message = "There was an error in the form submission. Please correct the errors below."
    else:
        form = SchoolTeamForm()
        error_message = None

    return render(
        request, "teams/new_team.html", {"form": form, "error_message": error_message}
    )


# @school_required
def update_team(request, id):
    team = get_object_or_404(SchoolTeam, id=id)

    if request.method == "POST":
        form = SchoolTeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect("teams")  # Redirect to the team list page or another URL
    else:
        form = SchoolTeamForm(instance=team)

    return render(request, "teams/update_team.html", {"form": form, "team": team})


# # view team details


def team_details(request, id):
    team = SchoolTeam.objects.get(id=id)
    athletes = team.athletes.all()
    context = {"team": team, "athletes": athletes}
    return render(request, "teams/team.html", context)


def teamlist(request):
    school_instance = get_object_or_404(School, user=request.user)

    teams = SchoolTeam.objects.filter(school=school_instance)

    context = {"teams": teams}
    return render(request, "teams/teams.html", context)


# # delete team
@school_required
def delete_team(request, id):
    team = get_object_or_404(SchoolTeam, pk=id)

    if request.method == "POST":
        team.delete()
        return redirect("teams")  # Redirect to the team list page or another URL

    return render(request, "teams/delete_team.html", {"team": team})


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


def generate_sdalbum(request, id):

    team = SchoolTeam.objects.get(id=id)
    athletes = team.athletes.all()

    # Get template
    template = get_template("albums/albums.html")

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
        "team": team,
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