from django.shortcuts import render
from school.models import *

from accounts.decorators import (

    staff_required,

)



# Create your views here.
@staff_required
def Overview(request):
    # today = timezone.now().date()
    schools = School.objects.all()
    active_athletes = Athlete.objects.filter(status="ACTIVE").count()
    schools_count = School.objects.all().count
    # schools_today = School.objects.filter(created_at__date=today).count
    athletes = Athlete.objects.all()
    athletes_count = Athlete.objects.all().count
    officials_count = school_official.objects.all().count
    athletes_bcount = Athlete.objects.filter(gender="male").count
    athletes_gcount = Athlete.objects.filter(gender="female").count
    officials_bcount = school_official.objects.filter(gender="M").count
    officials_gcount = school_official.objects.filter(gender="F").count
    # greeting = get_greeting()
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
        "active_athletes": active_athletes,
        # # "greeting": greeting,
    }
    return render(request, "dashboard/analytics.html", context)

