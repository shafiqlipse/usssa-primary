from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from accounts.decorators import school_required, anonymous_required, staff_required
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from .models import User
from django.contrib import messages
from .forms import SchoolRegistrationForm
from dashboard.models import school_official, School


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


from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib import messages

# from accounts.forms import AthleteFilterForm

from django.contrib.auth.decorators import login_required


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

# from dashboard.models import Athlete

# from django.http import FileResponse
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image
# from reportlab.lib import colors
# import io


# def create_athlete_card(p, athlete, x, y):
#     # Draw a border for the card
#     p.rect(x, y, 240, 150)

#     # Add image to the card on the left
#     if athlete.photo:
#         image_path = athlete.photo.path
#         p.drawInlineImage(image_path, x + 10, y + 70, width=100, height=60)

#     # Add athlete information to the card on the right
#     p.drawString(
#         x + 120, y + 130, f"Name: {athlete.fname} {athlete.lname}"
#     )
#     p.drawString(x + 120, y + 110, f"ID: {athlete.lin}")
#     p.drawString(x + 120, y + 90, f"Classroom: {athlete.classroom}")
#     p.drawString(x + 120, y + 70, f"Sport: {athlete.sport}")
#     p.drawString(x + 120, y + 50, f"Age: {athlete.age}")
#     p.drawString(x + 120, y + 30, f"Gender: {athlete.gender}")


# def some_view(request):
#     # Create a file-like buffer to receive PDF data.
#     buffer = io.BytesIO()

#     # Create the PDF object, using the buffer as its "file."
#     p = canvas.Canvas(buffer, pagesize=A4)
#     width, height = A4

#     # Set starting position for the first card
#     x_start = 20
#     y_start = height - 20 - 150  # Start from 20px below the top of the page

#     # Draw things on the PDF. Here's where the PDF generation happens.
#     athletes = Athlete.objects.all()

#     # Iterate through each athlete and create a card
#     for i, athlete in enumerate(athletes):
#         # Calculate the position for the current card
#         x = (
#             x_start + (i % 2) * 260
#         )  # 260 is the width of each card plus 20 units spacing
#         y = y_start - (i // 2) * 170  # 170 is the height of each card plus some spacing

#         create_athlete_card(p, athlete, x, y)

#         # Start a new page after every 8 cards
#     if i > 0 and i % 7 == 0:
#         p.showPage(top=height)  # Start new page at top of the page
#         y_start = 20  # Adjust the starting y-coordinate for the new page

#     # Save the PDF
#     p.save()

#     # FileResponse sets the Content-Disposition header so that browsers
#     # present the option to save the file.
#     buffer.seek(0)
#     return FileResponse(buffer, as_attachment=True, filename="athlete_cards.pdf")


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
