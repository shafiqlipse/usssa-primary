from django.shortcuts import render, redirect, get_object_or_404
from core.forms import *
from .forms import *
from core.models import *
import base64
from django.core.files.base import ContentFile
from django.contrib import messages
from accounts.decorators import admin_required

from django.conf import settings
from django.db import IntegrityError
# Create your views here.

def add_sports_officer(request):

    if request.method == "POST":
        form = SportsOfficerForm(request.POST, request.FILES)

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
        form = SportsOfficerForm()

    context = {"form": form}
    return render(request, "sportsofficers/newofficial.html", context)


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
    officers = SportsOfficer.objects.filter()
    context = {"officers": officers}
    return render(request, "sportsofficers/officers.html", context)


def Aofficers(request):
    officers = SportsOfficer.objects.filter(status="Inactive")
    context = {"officers": officers}
    return render(request, "sportsofficers/officers.html", context)

from django.http import JsonResponse
def activate_officer(request, id):
    officer = get_object_or_404(SportsOfficer, id=id)
    officer.status = "Active"
    officer.save()
    response_data = {"message": "School activated successfully."}
    return JsonResponse(response_data)


def District_officers(request):
    tofficers = TeamOfficer.objects.all()
    context = {"tofficers": tofficers}
    return render(request, "tofficers/tofficers.html", context)


def team_officers(request):
    officer = get_object_or_404(SportsOfficer, user=request.user)
    tofficers = TeamOfficer.objects.filter(user = officer.user)
    
    if request.method == "POST":
        form = TOfficerForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                tofficer = form.save(commit=False)
                # assign sports officer
                tofficer.user = officer.user
                # handle cropped image
                cropped_data = request.POST.get("photo_cropped")
                
                if cropped_data:
                    try:
                        format, imgstr = cropped_data.split(";base64,")
                        ext = format.split("/")[-1]
                        data = ContentFile(base64.b64decode(imgstr), name=f"photo.{ext}")
                        tofficer.photo = data
                    except (ValueError, TypeError):
                        messages.error(request, "Invalid image data.")
                        return render(request, "tofficers/tofficers.html", {"form": form, "tofficers":  officer})

                tofficer.save()
                return redirect("team_officers")
            except IntegrityError as e:
                if "nin" in str(e).lower():
                    messages.error(
                        request,
                        "An official with this Learner Identification Number (LIN) already exists.",
                    )
                else:
                    messages.error(request, f"Error adding official: {str(e)}")
    else:
        form = TOfficerForm()

# Prefill form with existing data

    context = {"tofficers": tofficers, "form": form}
    return render(request, "tofficers/tofficers.html", context)


def tofficer_details(request, id):
    tofficer = TeamOfficer.objects.get(id=id)

    context = {"tofficer": tofficer}
    return render(request, "tofficers/tofficera.html", context)


def officer_details(request, id):
    officer = SportsOfficer.objects.get(id=id)
    user = officer.user
    officers = TeamOfficer.objects.filter(user=user)

    context = {"officer": officer, "officers": officers}
    return render(request, "sportsofficers/officer.html", context)


# # delete team


def delete_officer(request, id):
    officer = get_object_or_404(SportsOfficer, id=id)

    if request.method == "POST":
        officer.delete()
        return redirect("tofficers")  # Redirect to the team list page or another URL

    return render(request, "officer/delete_team.html", {"officer": officer})

# # delete team


def delete_tofficer(request, id):
    officer = get_object_or_404(TeamOfficer, id=id)

    if request.method == "POST":
        officer.delete()
        return redirect("officers")  # Redirect to the team list page or another URL

    return render(request, "tofficers/delete_tofficer.html", {"officer": officer})





# @school_required
def Officerdash(request):
    user = request.user
    officer = SportsOfficer.objects.get(user_id=user.id)
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
    return render(request, "sportsofficers/dprofile.html", context)
# @school_required
def district_schools(request):
    user = request.user
    officer = SportsOfficer.objects.get(user_id=user.id)
    district = officer.district
    schools = School.objects.filter(district=district)
    

    context = {
        "officer": officer,
        "district": district,
        "schools": schools,
       
    }
    return render(request, "horizon/schools.html", context)
# @school_required
def district_athletes(request):
    user = request.user
    officer = SportsOfficer.objects.get(user_id=user.id)
    district = officer.district
    schools = School.objects.filter(district=district)
    athletes = Athlete.objects.filter(school__in=schools,status = "ACTIVE")
    

    context = {
        "officer": officer,
        "district": district,
        "schools": schools,
        "athletes": athletes,
    
    }
    return render(request, "horizon/athletes.html", context)
# @school_required
def Officewrdash(request):
    user = request.user
    officer = SportsOfficer.objects.get(user_id=user.id)
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

