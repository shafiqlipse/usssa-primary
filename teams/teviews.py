from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Create your views here.

def get_athletes(request):
    user = request.user
    school = get_object_or_404(School, user=user)

    gender = request.GET.get("gender")
    age_id = request.GET.get("age_id")

    athletes = Athlete.objects.filter(school=school)

    if gender:
        athletes = athletes.filter(gender=gender)

    if age_id:
        athletes = athletes.filter(age_id=age_id)

    athletes = athletes.values("id", "fname", "lname")
    data = {"athletes": list(athletes)}

    return JsonResponse(data)


# def activate_team(request, id):
#     team = get_object_or_404(SchoolTeam, id=id)
#     team.status = "Active"
#     team.save()
#     response_data = {"message": "School activated successfully."}
#     return JsonResponse(response_data)


# def deactivate_team(request, id):
#     team = get_object_or_404(SchoolTeam, id=id)
#     team.status = "Inactive"
#     team.save()
#     response_data = {"message": "School activated successfully."}
#     return JsonResponse(response_data)
