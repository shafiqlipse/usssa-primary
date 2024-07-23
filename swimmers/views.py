from django.shortcuts import render, redirect
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
from .filters import swimmerFilter  # Assume you have created this filter
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

# Create your views here.
from .models import *
from .forms import *
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

def swimmera(request):

    if request.method == "POST":
        form = SwimmerForm(request.POST, request.FILES)

        if form.is_valid():
            # admin_user = User.objects.get_or_create(username="admin")
            # Assign the currently logged-in user
            form.save()
            messages.success(request, "Account completed successfully!")
            return redirect("ofifcom")

        else:
            # Add form-specific error messages for individual fields
            messages.error(request, "Form is not valid. Please check your input.")
            print(f"Form errors: {form.errors}")

    else:
        form = SwimmerForm()

    context = {"form": form}
    return render(request, "swimmer_new.html", context)


def swimmers(request):
    # Get all swimmers
    swimmers = Swimmer.objects.all()

    # Apply the filter
    swimmer_filter = swimmerFilter(request.GET, queryset=swimmers)
    filtered_swimmers = swimmer_filter.qs

    if request.method == "POST":
        # Generate PDF
        template = get_template("acred.html")
        context = {"swimmers": filtered_swimmers}
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
        return render(request, "swimmers.html", {"filter": swimmer_filter})


def swimmer_details(request, id):
    swimmer = Swimmer.objects.get(id=id)

    context = {"swimmer": swimmer}
    return render(request, "swimmer.html", context)


def delete_swimmer(request, id):
    swimmer = get_object_or_404(Swimmer, id=id)
    
    if request.method == 'POST':
        swimmer.delete()
        messages.success(request, f"Swimmer {swimmer.first_name} {swimmer.last_name} has been deleted.")
        return redirect('swimmers')  # Redirect to the list of swimmers
    
    context = {"swimmer": swimmer}
    return render(request, "delete_swimmer.html", context)