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


def Teachera(request):

    if request.method == "POST":
        form = TeacherForm(request.POST, request.FILES)

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
        form = TeacherForm()

    context = {"form": form}
    return render(request, "teacher_new.html", context)


def Teachers(request):
    teachers = Teacher.objects.all()
    context = {"teachers": teachers}
    return render(request, "teachers.html", context)


from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from PyPDF2 import PdfReader, PdfWriter
import math
import zipfile


def teccreditation(request):
    teachers = Teacher.objects.all()
    template = get_template("acred.html")
    context = {"teachers": teachers}
    html = template.render(context)

    # Create a PDF in memory
    pdf_buffer = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf_buffer)

    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    pdf_buffer.seek(0)

    # Split the PDF into segments
    reader = PdfReader(pdf_buffer)
    total_pages = len(reader.pages)
    pages_per_segment = 500  # Adjust this value as needed
    num_segments = math.ceil(total_pages / pages_per_segment)

    response = HttpResponse(content_type="application/zip")
    response["Content-Disposition"] = (
        'attachment; filename="Accreditation_Segments.zip"'
    )

    with zipfile.ZipFile(response, "w") as zip_file:
        for i in range(num_segments):
            start_page = i * pages_per_segment
            end_page = min((i + 1) * pages_per_segment, total_pages)

            writer = PdfWriter()
            for page_num in range(start_page, end_page):
                writer.add_page(reader.pages[page_num])

            segment_buffer = BytesIO()
            writer.write(segment_buffer)
            segment_buffer.seek(0)

            zip_file.writestr(
                f"Accreditation_Segment_{i+1}.pdf", segment_buffer.getvalue()
            )

    return response


def teacher_details(request, id):
    teacher = Teacher.objects.get(id=id)

    context = {"teacher": teacher}
    return render(request, "teacher.html", context)
