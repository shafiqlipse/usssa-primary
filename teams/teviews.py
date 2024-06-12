from .models import *
from .forms import *
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404

# Create your views here.


def get_athletes(request):
    user = request.user
    school = get_object_or_404(School, user=user)

    sport_id = request.GET.get("sport_id")
    gender = request.GET.get("gender")
    age_id = request.GET.get("age_id")

    athletes = Athlete.objects.filter(school=school)

    if sport_id:
        athletes = athletes.filter(sport_id=sport_id)

    if gender:
        athletes = athletes.filter(gender=gender)

    if age_id:
        athletes = athletes.filter(age_id=age_id)

    athletes = athletes.values("id", "fname")
    data = {"athletes": list(athletes)}

    return JsonResponse(data)
