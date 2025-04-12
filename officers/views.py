from django.shortcuts import render, redirect, get_object_or_404
from core.forms import *
from .forms import *
from core.models import *
import base64
from django.core.files.base import ContentFile
from django.contrib import messages
from accounts.decorators import admin_required
# Create your views here.

@admin_required
def profile_update(request, id):
    officer = get_object_or_404(Officer, id=id)

    if request.method == "POST":
        form = OfficerForm(request.POST, request.FILES, instance=officer)
        if form.is_valid():
            # Process the cropped image data if it's provided
            cropped_data = request.POST.get("photo_cropped")
            if cropped_data:
                try:
                    format, imgstr = cropped_data.split(";base64,")
                    ext = format.split("/")[-1]
                    data = ContentFile(base64.b64decode(imgstr), name=f"photo.{ext}")
                    officer.photo = data  # Assign cropped image to the officer's photo field
                except (ValueError, TypeError) as e:
                    messages.error(request, "Invalid image data.")
                    return render(request, "editprofile.html", {"form": form, "officer": officer})

            # Save the form after handling the image
            form.save()
            officer.save()  # Save the officer object with the new photo (if provided)
            return redirect("officer_dashboard")
    else:
        form = OfficerForm(instance=officer)

    context = {"form": form, "officer": officer}
    return render(request, "editprofile.html", context)

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
    return render(request, "officer/newofficial.html", context)


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
    return render(request, "officer/tofficer.html", context)


def officers(request):
    officers = Officer.objects.all()
    context = {"officers": officers}
    return render(request, "officer/officers.html", context)


def Dofficers(request):
    tofficers = TOfficer.objects.all()
    context = {"tofficers": tofficers}
    return render(request, "officer/tofficers.html", context)


def tofficers(request):
    officer = get_object_or_404(Officer, user=request.user)
    tofficers = TOfficer.objects.filter(user = officer.user)
    
    if request.method == "POST":
        form = TOfficerForm(request.POST, request.FILES)  # Update instance
        if form.is_valid():
            # Process the cropped image data if provided
            cropped_data = request.POST.get("photo_cropped")
            if cropped_data:
                try:
                    format, imgstr = cropped_data.split(";base64,")
                    ext = format.split("/")[-1]
                    data = ContentFile(base64.b64decode(imgstr), name=f"photo.{ext}")
                    officer.photo = data  # Assign cropped image to officer's photo field
                    officer.save()  # Save the updated officer instance
                except (ValueError, TypeError):
                    messages.error(request, "Invalid image data.")
                    return render(request, "editprofile.html", {"form": form, "officer": officer})

            form.save()
            return redirect("officer_dashboard")
    else:
        form = TOfficerForm()  # Prefill form with existing data

    context = {"tofficers": tofficers, "form": form}
    return render(request, "tofficers/tofficers.html", context)


def tofficer_details(request, id):
    tofficer = TOfficer.objects.get(id=id)

    context = {"tofficer": tofficer}
    return render(request, "officer/tofficera.html", context)


def officer_details(request, id):
    officer = Officer.objects.get(id=id)

    context = {"officer": officer}
    return render(request, "officer/officer.html", context)


# # delete team


def delete_officer(request, id):
    officer = get_object_or_404(Officer, id=id)

    if request.method == "POST":
        officer.delete()
        return redirect("officers")  # Redirect to the team list page or another URL

    return render(request, "officer/delete_team.html", {"officer": officer})


def district(request):
    officer = request.user
    if officer.is_district:
        location = get_object_or_404(District, id=officer.district_id)
        schools = School.objects.filter(district=location)

    else:
        location = get_object_or_404(City, id=officer.city_id)
        schools = School.objects.filter(city=location)

    athletes = Athlete.objects.filter(officer__in=schools)
    context = {"location": location, "schools": schools, "athletes": athletes}
    return render(request, "district_template.html", context)


from django.shortcuts import render
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import *
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.http import HttpResponseRedirect
from django.urls import reverse
from xhtml2pdf import pisa

def dTeams(request):
    # Get officer from user profile
    
    user = request.user
    officer = Officer.objects.get(user_id=user.id) # Assuming profile has officer attribute

    # Get all enrollments for the officer
    enrollments = Team.objects.filter(team_officer=user).annotate(
        athlete_count=Count('team_athletes__athletes')
    )

    if request.method == "POST":
        form = TeamForm(request.POST, request.FILES)

        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.team_officer = user
            enrollment.save()
            messages.success(request, "Enrollment created successfully!")
            return redirect("district_enrollments")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeamForm()

    context = {"form": form, "enrollments": enrollments}
    return render(request, "enrollments/officer_enrolls.html", context)

def dAllEnrollments(request):
    # Get all officer_enrolls with athlete count
    officer_enrolls = Team.objects.annotate(
        athlete_count=Count('team_athletes__athletes')
    )

    context = {
        "officer_enrolls": officer_enrolls,
    }

    return render(request, "enrollments/enroll.html", context)


def remove_athlete(request, enrollment_id, athlete_id):
    athlete_enrollment = get_object_or_404(AthletesEnrollment, id=enrollment_id)
    athlete = get_object_or_404(Athlete, id=athlete_id)

    if request.method == "POST":
        athlete_enrollment.athletes.remove(athlete)
        return HttpResponseRedirect(
            reverse("district_enrollment", args=[athlete_enrollment.team.id])
        )

    return redirect(
        "enrollments/officer_enrollment", id=athlete_enrollment.team.id
    )


def officer_enrollment_details(request, id):
    officer_enrollment = get_object_or_404(Team, id=id)
    officer = Officer.objects.get(user=request.user)
    location = officer.district

    schools = School.objects.filter(district=location)
    # Start with the base queryset for athletes in the user's schools
    # athletes = Athlete.objects.filter()
    
    if request.method == "POST":
        form = AthleteEnrollmentForm(request.POST)
        if form.is_valid():
            athlete_enrollment = AthletesEnrollment.objects.create(
                team=officer_enrollment
            )
            athlete_enrollment.athletes.set(form.cleaned_data["athletes"])
            return HttpResponseRedirect(reverse("district_enrollment", args=[id]))
    else:
        form = AthleteEnrollmentForm()

    athlete_enrollments = AthletesEnrollment.objects.filter(
        team=officer_enrollment
    )
    all_athletes = Athlete.objects.filter(school__in=schools, status="ACTIVE",age = officer_enrollment.team_age, gender = officer_enrollment.team_gender)

    context = {
        "officer_enrollment": officer_enrollment,
        "form": form,
        "athlete_enrollments": athlete_enrollments,
        "all_athletes": all_athletes,
    }
    return render(request, "enrollments/officer_enroll.html", context)


def officer_enrollment_update(request, id):
    officer_enrollment = get_object_or_404(Team, id=id)

    if request.method == "POST":
        form = TeamForm(
            request.POST, request.FILES, instance=officer_enrollment
        )
        if form.is_valid():
            form.save()
            messages.success(
                request, "Team information updated successfully!"
            )
            return redirect("officer_enrollment", id=officer_enrollment.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = TeamForm(instance=officer_enrollment)

    context = {
        "form": form,
        "officer_enrollment": officer_enrollment,
    }
    return render(request, "enrollments/update_officer_enroll.html", context)


def officer_enroll_delete(request, id):
    stud = Team.objects.get(id=id)
    if request.method == "POST":
        stud.delete()
        return redirect("district_enrollments")

    return render(request, "enrollments/delete_officer_enroll.html", {"obj": stud})


from django.shortcuts import render
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template

from xhtml2pdf import pisa

# Make sure to import your models

admin_required


def dAccreditation(request, id):
    team = get_object_or_404(Team, id=id)
    athlete_enrollments = AthletesEnrollment.objects.filter(team=team)
    athletes = Athlete.objects.filter(athletesenrollment__in=athlete_enrollments)

    # Get template
    template = get_template("reports/acred.html")

    # Compress and fix rotation for athletes' photos

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
    response["Content-Disposition"] = 'attachment; filename="Accreditation.pdf"'

    # Generate PDF from HTML
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    return response


def dAlbums(request, id):
    team = get_object_or_404(Team, id=id)
    athlete_enrollments = AthletesEnrollment.objects.filter(team=team)
    athletes = Athlete.objects.filter(athletesenrollment__in=athlete_enrollments)


    # Get athlete and official counts
    athlete_count = athletes.count()


    # Create a unique filename
    filename = f"{team.team_officer.officer_profile.first().district } | {team.team_sport} .pdf"

    # Get template
    template = get_template("reports/albums.html")

    # Prepare context
    context = {
        "team": team,
        "athlete_count": athlete_count,
        "athletes": athletes,
        "MEDIA_URL": settings.MEDIA_URL,
    }

    # Render HTML
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    # Generate PDF from HTML
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    return response


admin_required


def dCertificate(request, id):
    team = get_object_or_404(Team, id=id)
    athlete_enrollments = AthletesEnrollment.objects.filter(officer_enrollment=team)
    athletes = Athlete.objects.filter(athleteenrollment__in=athlete_enrollments)

    # Get template
    template = get_template("reports/cert.html")

    # Compress and fix rotation for athletes' photos

    # Prepare context
    context = {
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


