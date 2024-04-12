from django.shortcuts import render, redirect
from django.contrib.auth import logout, login
from accounts.decorators import school_required, anonymous_required, staff_required
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
from reportlab.lib import colors
import io
from django.contrib import messages
from .forms import SchoolRegistrationForm
from dashboard.models import school_official, School, Athlete
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash


# from accounts.forms import AthleteFilterForm


@staff_required
def school_registration(request):
    if request.method == "POST":
        form = SchoolRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(
                commit=False
            )  # Create the user object without saving to the database
            user.is_school = True  # Set is_school to True
            user.save()  # Save the user object with is_school set to True

            # Log in the user
            login(request, user)

            return redirect("confirmation")
    else:
        form = SchoolRegistrationForm()
    return render(request, "register.html", {"form": form})


# Create your views here.
@anonymous_required
def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Get the user without logging in
            user = form.get_user()
            login(request, user)

            # Check if the user is a school and has a school profile
            if user.is_school:
                try:
                    school = School.objects.get(user=user)
                    return redirect(
                        "school_dashboard"
                    )  # Adjust the URL name for your school dashboard view
                except School.DoesNotExist:
                    return redirect(
                        "new_school"
                    )  # Adjust the URL name for your create school view

            # If the user is not a school, log in and redirect to dashboard
            messages.success(request, "Login successful.")
            return redirect("dashboard")  # Adjust the URL name for your dashboard view
        else:
            messages.error(request, "Error in login. Please check your credentials.")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def user_logout(request):
    # if user.is_authenticated:
    logout(request)
    return redirect("login")


def custom_404(request, exception):
    return render(request, "account/custom404.html", {}, status=404)


from django.shortcuts import render
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse
from django.contrib.staticfiles import finders
import base64
from django.conf import settings


def generate_scalbum(request, id):

    school = School.objects.get(id=id)
    athletes = Athlete.objects.filter(school=school)
    # Get template
    # Get template
    image_path = finders.find("images/upsa.png")

    # Read the image file and encode it as base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    # Get template
    template = get_template("accounts/Albums.html")

    context = {"athletes": athletes, "school": school, "MEDIA_URL": settings.MEDIA_URL}
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Album.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


def generate_album(request):
    user = request.user
    school = user.school_profile.first()
    athletes = Athlete.objects.filter(school=school)
    # Get template
    # Get template
    image_path = finders.find("images/upsa.png")

    # Read the image file and encode it as base64
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    # Get template
    template = get_template("accounts/Albums.html")

    context = {"athletes": athletes, "school": school, "MEDIA_URL": settings.MEDIA_URL}
    html = template.render(context)

    # Create a PDF
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="Album.pdf"'

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


def album(request):
    user = request.user
    school = user.school_profile.first()
    athletes = Athlete.objects.filter(school=school)
    context = {"athletes": athletes, "school": school}
    return render(request, "accounts/Albums.html", context)


#  auth views
@anonymous_required
def school_registration(request):
    if request.method == "POST":
        form = SchoolRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(
                commit=False
            )  # Create the user object without saving to the database
            user.is_school = True  # Set is_school to True
            user.save()  # Save the user object with is_school set to True

            # Log in the user
            login(request, user)

            return redirect("new_school")
    else:
        form = SchoolRegistrationForm()
    return render(request, "register.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Update the session to maintain the user's login status
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("login")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "change_password.html", {"form": form})


# reportlab pdf generation of reports certificates and albums
from django.shortcuts import get_object_or_404


def activate_school(request, id):
    school = get_object_or_404(School, id=id)
    school.status = "Active"
    school.save()
    return HttpResponse("School activated successfully.")


# from django.http import HttpResponse
# from django.template.loader import render_to_string
# import pdfkit

# def generate_album(request):
#     # Retrieve school data from the database
#     user = request.user
#     school = user.school_profile.first()

#     # Render HTML template with school data
#     html_content = render_to_string('accounts/Albums.html', {'school': school})

#     # Generate PDF from HTML content
#     pdf = pdfkit.from_string(html_content, False)

#     # Return PDF as a downloadable attachment
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="{school.name}_profile.pdf"'
#     return response


# @login_required(login_url="login")
# def album(request):
# if request.method == 'POST':
#     form = AthleteFilterForm(request.POST)
#     if form.is_valid():
#         selected_school = form.cleaned_data['school']
#         selected_tournament = form.cleaned_data['tournament']

#         athletes = Athlete.objects.filter(school=selected_school, tournament=selected_tournament)
#         officials = school_official.objects.filter(school=selected_school)

#         return render(request, 'filtered_results.html', {'athletes': athletes, 'officials': officials})

# else:
#     form = AthleteFilterForm()

# return render(request, 'filter_album.html', {'form': form})


# views.py
# import requests
# from django.shortcuts import render, redirect
# from .models import Payment

# def initiate_payment(request):
#     if request.method == 'POST':
#         amount = request.POST.get('amount')
#         description = request.POST.get('description')
#         phone_number = request.POST.get('phone_number')

#         # Determine the payment provider based on the phone number
#         payment_provider = determine_payment_provider(phone_number)

#         # Create a new payment record in the database
#         payment = Payment.objects.create(
#             amount=amount,
#             description=description,
#             phone_number=phone_number,
#             payment_provider=payment_provider
#         )

#         # TODO: Integrate with the respective payment service API based on payment_provider
#         api_url = get_payment_api_url(payment_provider)
#         api_key = get_payment_api_key(payment_provider)
#         response = make_payment_request(api_url, api_key, amount, phone_number, description)

#         # Process the API response (handle success, failure, etc.)
#         if response.status_code == 200:
#             # Payment successful, update the payment status in the database
#             payment.status = 'completed'
#             payment.save()
#             return redirect('payment_success')
#         else:
#             # Payment failed, handle accordingly
#             payment.status = 'failed'
#             payment.save()
#             return redirect('payment_failure')

#     return render(request, 'initiate_payment.html')
# # views.py (continued)
# def make_payment_request(api_url, api_key, amount, phone_number, description):
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {api_key}',
#     }

#     payload = {
#         'amount': amount,
#         'phone_number': phone_number,
#         'description': description,
#     }

#     response = requests.post(api_url, json=payload, headers=headers)
#     return response

# def get_payment_api_url(payment_provider):
#     # Provide the actual API URLs based on payment provider
#     if payment_provider == 'airtel':
#         return 'https://api.airtelmoney.com/payment'
#     elif payment_provider == 'mtn':
#         return 'https://api.mtnmomo.com/payment'
#     # Add other cases as needed

# def get_payment_api_key(payment_provider):
#     # Provide the actual API keys based on payment provider
#     if payment_provider == 'airtel':
#         return 'your_airtel_api_key'
#     elif payment_provider == 'mtn':
#         return 'your_mtn_api_key'
#     # Add other cases as needed
# form dashboard.models import Athlete


def reg_athletes(request):
    user = request.user
    school_profile = user.school_profile.first()
    if school_profile:
        school_id = school_profile.id
        athletes = Athlete.objects.filter(school_id=school_id)
        for athlete in athletes:
            athlete.amount = 1500
    else:
        athletes = Athlete.objects.none()

    if request.method == "POST":
        selected_athletes = request.POST.getlist("selected_athletes")
        number_of_athletes = int(request.POST.get("number_of_athletes", 0))
        total_amount = number_of_athletes * 1500
        return render(request, "accounts/payment.html", {"total_amount": total_amount})

    context = {
        "athletes": athletes,
    }

    return render(request, "accounts/registration.html", context)
