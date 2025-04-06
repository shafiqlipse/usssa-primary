from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib import messages
from xhtml2pdf import pisa
from io import BytesIO
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from accounts.decorators import admin_required

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.db.models import Count

from .filters import SchoolEnrollmentFilter  # Assume you have created this filter

# schools list, tuple or array
import json
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import User
from django.db.models import Q
def enrolls_data(request):
    """ Handle AJAX DataTables request for large datasets """

    try:
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get("search[value]", "")

        # Fetch and filter users
        teams_query = SchoolEnrollment.objects.annotate(athlete_count=Count('athlete_enrollments__athletes'))

        # Apply search across multiple fields
        if search_value:
            teams_query = teams_query.filter(
                Q(school__icontains=search_value) |
                Q(championship__icontains=search_value) |
                Q(sport__icontains=search_value) 
    # Search EMIS
            )

        # Paginate results
        paginator = Paginator(teams_query, length)
        page_number = (start // length) + 1
        enrolls_page = paginator.get_page(page_number)

        # Prepare JSON response
        data = []
        for team in enrolls_page:
            school = team.school
            championship = team.championship
            sport = team.sport


            action_buttons = f"""
                
                <a href="/dashboard/user/edit/{team.id}/" class="btn btn-primary btn-sm">Album</a>
                <a href="/dashboard/user/edit/{team.id}/" class="btn btn-warning btn-sm">Accrediation</a>
                <a href="/dashboard/user/edit/{team.id}/" class="btn btn-info btn-sm">Certificate</a>
                
            """

            data.append({
                "school": school,
                "championship": championship,
                "championship": sport,
                "actions": action_buttons,
            })

        response = {
            "draw": draw,
            "recordsTotal": SchoolEnrollment.objects.all().count(),
            "recordsFiltered": teams_query.count(),
            "data": data,
        }

        return JsonResponse(response)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



def SchoolEnrollments(request):
    # Get school from user profile
    
    user = request.user
    school = School.objects.get(user_id=user.id) # Assuming profile has school attribute

    # Get all enrollments for the school
    enrollments = SchoolEnrollment.objects.filter(school=school).annotate(
        athlete_count=Count('athlete_enrollments__athletes')
    )

    if request.method == "POST":
        form = SchoolEnrollmentForm(request.POST, request.FILES)

        if form.is_valid():
            enrollment = form.save(commit=False)
            enrollment.school = school
            enrollment.save()
            messages.success(request, "Enrollment created successfully!")
            return redirect("school_enrollments")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SchoolEnrollmentForm()

    context = {"form": form, "enrollments": enrollments}
    return render(request, "enrollments/school_enrolls.html", context)

def AllEnrollments(request):
    # Get all school_enrolls with athlete count
    school_enrolls = SchoolEnrollment.objects.annotate(
        athlete_count=Count('athlete_enrollments__athletes')
    )

    context = {
        "school_enrolls": school_enrolls,
    }

    return render(request, "enrollments/enroll.html", context)


def remove_athlete(request, enrollment_id, athlete_id):
    athlete_enrollment = get_object_or_404(AthleteEnrollment, id=enrollment_id)
    athlete = get_object_or_404(Athlete, id=athlete_id)

    if request.method == "POST":
        athlete_enrollment.athletes.remove(athlete)
        return HttpResponseRedirect(
            reverse("school_enrollment", args=[athlete_enrollment.school_enrollment.id])
        )

    return redirect(
        "enrollments/school_enrollment", id=athlete_enrollment.school_enrollment.id
    )


def school_enrollment_details(request, id):
    school_enrollment = get_object_or_404(SchoolEnrollment, id=id)
    school = school_enrollment.school
    if request.method == "POST":
        form = AthleteEnrollmentForm(request.POST)
        if form.is_valid():
            athlete_enrollment = AthleteEnrollment.objects.create(
                school_enrollment=school_enrollment
            )
            athlete_enrollment.athletes.set(form.cleaned_data["athletes"])
            return HttpResponseRedirect(reverse("school_enrollment", args=[id]))
    else:
        form = AthleteEnrollmentForm()

    athlete_enrollments = AthleteEnrollment.objects.filter(
        school_enrollment=school_enrollment
    )
    all_athletes = Athlete.objects.filter(school=school, status="ACTIVE", gender = school_enrollment.gender)

    context = {
        "school_enrollment": school_enrollment,
        "form": form,
        "athlete_enrollments": athlete_enrollments,
        "all_athletes": all_athletes,
    }
    return render(request, "enrollments/school_enroll.html", context)


def school_enrollment_update(request, id):
    school_enrollment = get_object_or_404(SchoolEnrollment, id=id)

    if request.method == "POST":
        form = SchoolEnrollmentForm(
            request.POST, request.FILES, instance=school_enrollment
        )
        if form.is_valid():
            form.save()
            messages.success(
                request, "SchoolEnrollment information updated successfully!"
            )
            return redirect("school_enrollment", id=school_enrollment.id)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SchoolEnrollmentForm(instance=school_enrollment)

    context = {
        "form": form,
        "school_enrollment": school_enrollment,
    }
    return render(request, "enrollments/update_school_enroll.html", context)


def school_enroll_delete(request, id):
    stud = SchoolEnrollment.objects.get(id=id)
    if request.method == "POST":
        stud.delete()
        return redirect("school_enrollments")

    return render(request, "enrollments/delete_school_enroll.html", {"obj": stud})


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


def Accreditation(request, id):
    team = get_object_or_404(SchoolEnrollment, id=id)
    athlete_enrollments = AthleteEnrollment.objects.filter(school_enrollment=team)
    athletes = Athlete.objects.filter(athleteenrollment__in=athlete_enrollments)

    # Get template
    template = get_template("reports/acred.html")

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


def Albums(request, id):
    team = get_object_or_404(SchoolEnrollment, id=id)
    athlete_enrollments = AthleteEnrollment.objects.filter(school_enrollment=team)
    athletes = Athlete.objects.filter(athleteenrollment__in=athlete_enrollments)
    school = team.school
    officials = school_official.objects.filter(school=school)

    # Get athlete and official counts
    athlete_count = athletes.count()
    official_count = officials.count()

    # Create a unique filename
    filename = f"{team.school} | {team.sport} .pdf"

    # Get template
    template = get_template("reports/albums.html")

    # Prepare context
    context = {
        "team": team,
        "official_count": official_count,
        "athlete_count": athlete_count,
        "athletes": athletes,
        "officials": officials,
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


def Certificate(request, id):
    team = get_object_or_404(SchoolEnrollment, id=id)
    athlete_enrollments = AthleteEnrollment.objects.filter(school_enrollment=team)
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





def activate_team(request, id):
    school_enrollment = get_object_or_404(SchoolEnrollment, id=id)
    school_enrollment.status = "Active"
    school_enrollment.save()
    return render(request, "activation_success.html", {"message": "School activated successfully."})






import csv
from django.http import HttpResponse

def export_ecsv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="enrollments.csv"'

    # Create a CSV writer object using the HttpResponse as the file.
    writer = csv.writer(response)

    # Write the header row
    writer.writerow(
        [
            "id",
            "School",
            "District",
            "Region",
            "Championship",
            "Sport",
            "Athlete Count",
        ]
    )  # Replace with your model's fields

    for obj in SchoolEnrollment.objects.all():
        athlete_count = obj.athlete_enrollments.aggregate(total=models.Count('athletes'))['total'] or 0
        writer.writerow(
            [
                obj.id,
                obj.school,
                obj.school.district,
                obj.school.region,
                obj.championship,
                obj.sport,
                athlete_count,
            ]
        ) 
        # Replace with your model's fields

    return response

