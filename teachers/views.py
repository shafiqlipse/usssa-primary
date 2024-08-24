from django.shortcuts import render, redirect

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
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
from .models import *
from .forms import *


import base64
from django.core.files.base import ContentFile


def Teachera(request):

    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES)

        if form.is_valid():
            new_athlete = form.save(commit=False)

            # Handle the cropped image
            cropped_image_data = request.POST.get("croppedImage")
            if cropped_image_data:
                format, imgstr = cropped_image_data.split(";base64,")
                ext = format.split("/")[-1]
                image_data = base64.b64decode(imgstr)
                new_athlete.photo = ContentFile(
                    image_data, name=f"athlete_{new_athlete.id}.{ext}"
                )

            new_athlete.save()
            messages.success(request, "Form submitted successfully.")
            return redirect("addteacher")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        form = TeacherForm()

    context = {"form": form}
    return render(request, "teacher_new.html", context)


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
import math
import zipfile

from .filters import TeacherFilter  # Assume you have created this filter


def Teachers(request):
    # Get all teachers
    teachers = Teacher.objects.all()

    # Apply the filter
    teacher_filter = TeacherFilter(request.GET, queryset=teachers)
    filtered_teachers = teacher_filter.qs

    if request.method == "POST":
        # Generate PDF
        template = get_template("acred.html")
        context = {"teachers": filtered_teachers}
        html = template.render(context)

        # Create a PDF
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)

        if pisa_status.err:
            return HttpResponse("We had some errors <pre>" + html + "</pre>")

        pdf_buffer.seek(0)

        # Return the PDF as a response
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            'attachment; filename="Filtered_Accreditation.pdf"'
        )
        response.write(pdf_buffer.getvalue())
        return response
    else:
        # Render the filter form
        return render(request, "teachers.html", {"filter": teacher_filter})


def teacher_details(request, id):
    teacher = Teacher.objects.get(id=id)

    context = {"teacher": teacher}
    return render(request, "teacher.html", context)
