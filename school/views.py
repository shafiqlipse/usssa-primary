from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from accounts.models import *
from accounts.forms import *
from .models import *
from .forms import *
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError
from accounts.decorators import (
    school_required,
    staff_required,
    login_required,
)
import datetime
from django.core.files.base import ContentFile
import base64
# # Athletes details......................................................
# # Athletes details......................................................
from datetime import datetime

def get_greeting():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Good morning,"
    elif 12 <= current_hour < 17:
        return "Good afternoon,"
    elif 17 <= current_hour < 21:
        return "Good evening,"
    else:
        return "Good night,"


@school_required
def Dash(request):
    user = request.user
    school = School.objects.get(user_id=user.id)
    officials_count = school_official.objects.filter(school_id=school.id).count()
    athletes_count = Athlete.objects.filter(school_id=school.id).count()
    athletes = Athlete.objects.filter(school_id=school.id)[:6]
    officials_bcount = school_official.objects.filter(
        school_id=school.id, gender="M"
    ).count()
    officials_gcount = school_official.objects.filter(
        school_id=school.id, gender="F"
    ).count()
    athletes_gcount = Athlete.objects.filter(
        school_id=school.id, gender="Female"
    ).count()
    # teams_gcount = SchoolTeam.objects.filter(
    #     school_id=school.id, gender="Female"
    # # ).count()
    greeting = get_greeting()
    # teams_bcount = SchoolTeam.objects.filter(
    #     school_id=school.id, gender="Male"
    # # ).count()
    athletes_bcount = Athlete.objects.filter(school_id=school.id, gender="Male").count()
    officials = school_official.objects.filter(school_id=school.id)
    # teams = SchoolTeam.objects.filter(school_id=school.id).count

    # from django.contrib.auth.hashers import make_password

    context = {
        "officials_count": officials_count,
        "officials_bcount": officials_bcount,
        "officials_gcount": officials_gcount,
        "athletes_count": athletes_count,
        "athletes_bcount": athletes_bcount,
        "athletes_gcount": athletes_gcount,
        "officials": officials,
        "school": school,
        "athletes": athletes,
        "greeting": greeting
        # "teams": teams,
        # "teams_gcount": teams_gcount,
        # "teams_bcount": teams_bcount,
    }
    return render(request, "school/schoolprofile.html", context)



# # Athletes details......................................................
# # ..........................School............................

def schools(request):
    schools = School.objects.all()
    context = {
        "schools": schools,
        # "teamsFilter": teams
    }
    return render(request, "school/schools.html", context)


def Schoolnew(request):
    regions = Region.objects.all()

    if request.method == "POST":
        form = SchoolProfileForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Account completed successfully!")
                return redirect("confirmation")
            except IntegrityError as e:
                if "EMIS" in str(e):
                    messages.error(
                        request, "A school with this EMIS number already exists."
                    )
                else:
                    messages.error(
                        request,
                        "An error occurred while saving the school. Please fill all required fields.",
                    )
        else:
            # Add more detailed error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            print(f"Form errors: {form.errors}")

    else:
        form = SchoolProfileForm()

    context = {"form": form, "regions": regions}
    return render(request, "school/create_school.html", context)

@staff_required
def school_update(request, id):
    school = get_object_or_404(School, id=id)

    if request.method == "POST":
        form = SchoolEditForm(request.POST, instance=school)
        if form.is_valid():
            form.save()
            return redirect("schools")
    else:
        form = SchoolEditForm(instance=school)

    context = {"form": form, "school": school}
    return render(request, "dashboard/editschool.html", context)


@login_required
def schoolupdate(request, id):
    school = School.objects.get(id=id)

    if request.method == "POST":
        form = SchoolProfileForm(request.POST, instance=school)
        if form.is_valid():
            form.save()

            return redirect("school_dashboard")
    else:
        form = SchoolProfileForm(instance=school)
    context = {"form": form}
    return render(request, "school/create_school.html", context)


# @staff_required
@login_required
def school_detail(request, id):
    school = get_object_or_404(School, id=id)
    officials = school_official.objects.filter(school_id=id)
    athletes = Athlete.objects.filter(school_id=id)

    context = {
        "school": school,
        "athletes": athletes,
        "officials": officials,
    }
    return render(request, "school/school.html", context)



@login_required(login_url="login")
def DeleteSchool(request, id):
    stud = School.objects.get(id=id)
    if request.method == "POST":
        stud.delete()
        return redirect("schools")

    return render(request, "dashboard/deletesch.html", {"obj": stud})



# # Athletes details......................................................
# # ........................Athletes ..............................

# schools list, tuple or array
@staff_required
def all_athletes(request):

    athletes = Athlete.objects.all()

    context = {
        "athletes": athletes,
    }
    return render(request, "athletes/athletes.html", context)

# schools list, tuple or array

@login_required
def newAthlete(request):
    if request.method == "POST":
        form = NewAthleteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                new_athlete = form.save(commit=False)

                # Assign the school from the user profile
                new_athlete.school = (
                    request.user.school_profile.first()
                )  # Ensure profile has a school

                # Handle cropped image data for the "photo" field
                cropped_data = request.POST.get("photo_cropped")
                if cropped_data:
                    try:
                        format, imgstr = cropped_data.split(";base64,")
                        ext = format.split("/")[-1]
                        data = ContentFile(
                            base64.b64decode(imgstr), name=f"photo.{ext}"
                        )
                        new_athlete.photo = data  # Assign cropped image
                    except (ValueError, TypeError) as e:
                        messages.error(request, "Invalid image data.")
                        return render(
                            request, "athletes/newAthlete.html", {"form": form}
                        )

                new_athlete.save()
                messages.success(request, "Athlete added successfully!")
                return redirect("athletes")

            except IntegrityError as e:
                if "lin" in str(e).lower():
                    messages.error(
                        request,
                        "An athlete with this Learner Identification Number (LIN) already exists.",
                    )
                else:
                    messages.error(request, f"Error adding athlete: {str(e)}")
            except Exception as e:
                messages.error(request, f"Error adding athlete: {str(e)}")
        else:
            # Form validation error messages
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.capitalize()}: {error}")

    else:
        form = NewAthleteForm()

    return render(request, "athletes/newAthlete.html", {"form": form})

def calculate_age_choices(request):
    date_of_birth_str = request.GET.get("date_of_birth")

    # Check if date_of_birth_str is None
    if date_of_birth_str is None:
        return JsonResponse({"error": "Date of birth is missing"}, status=400)

    # Convert date_of_birth string to a datetime.date object
    date_of_birth = datetime.datetime.strptime(date_of_birth_str, "%Y-%m-%d").date()

    # Calculate the athlete's age based on the date of birth
    current_year = datetime.date.today().year
    calculated_age = (
        current_year
        - date_of_birth.year
        - (
            (datetime.date.today().month, datetime.date.today().day)
            < (date_of_birth.month, date_of_birth.day)
        )
    )

    # Filter the Age model to get age choices based on the calculated age
    age_choices = Age.objects.filter(
        min_age__lte=calculated_age, max_age__gte=calculated_age
    ).values_list("id", "name")

    # Prepare the JSON response
    response_data = {"ages": list(age_choices)}

    return JsonResponse(response_data)


# # Athletes details......................................................
@login_required
def AthleteDetail(request, id):
    athlete = get_object_or_404(Athlete, id=id)
    relatedathletes = Athlete.objects.filter(school=athlete.school).exclude(id=id)

    context = {
        "athlete": athlete,
        "relatedathletes": relatedathletes,
        # "breadcrumbs": breadcrumbs,
    }

    return render(request, "athletes/athlete.html", context)


@login_required(login_url="login")
def athletes(request):
    user = request.user
    school_profile = (
        user.school_profile.first()
    )  # Retrieve the first related School object
    if school_profile:
        school_id = school_profile.id
        athletes = Athlete.objects.filter(school_id=school_id)
    else:
        # Handle the case where the user is not associated with any school
        athletes = Athlete.objects.none()
    # officialFilter = OfficialFilter(request.GET, queryset=officials)

    context = {"athletes": athletes, "school_profile": school_profile}

    return render(request, "athletes/athletes.html", context)


@login_required
def AthleteUpdate(request, id):
    athlete = get_object_or_404(Athlete, id=id)

    if request.method == "POST":
        form = NewAthleteForm(request.POST, request.FILES, instance=athlete)
        if form.is_valid():
            form.save()
            messages.success(request, "Athlete information updated successfully!")
            return redirect("athletes")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = NewAthleteForm(instance=athlete)

    context = {
        "form": form,
        "athlete": athlete,
    }
    return render(request, "school/newAthlete.html", context)


def athlete_list(request):
    athletes = Athlete.objects.all()
    context = {"athletes": athletes}
    return render(request, "school/athlete_list.html", context)


# # Athletes details......................................................
# # ........................Officilas..............................

# schools list, tuple or array
@staff_required
def all_officials(request):

    officilas = school_official.objects.all()

    context = {
        "officilas": officilas,
    }
    return render(request, "officials/officials.html", context)


@school_required
def Official(request):
    if request.method == "POST":
        form = OfficialForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                official = form.save(commit=False)
                official.school = request.user.school_profile.first()
                official.save()
                messages.success(request, "Official added successfully!")
                return redirect("officials")
            except Exception as e:
                messages.error(request, f"Error adding athlete: {str(e)}")
        else:
            messages.error(request, "Form is not valid. Please check your input.")
    else:
        form = OfficialForm()

    context = {"form": form}
    return render(request, "officials/NOfficial.html", context)


@login_required(login_url="login")
def school_offs(request):
    user = request.user
    school_profile = (
        user.school_profile.first()
    )  # Retrieve the first related School object
    if school_profile:
        school_id = school_profile.id
        school_offs = school_official.objects.filter(school_id=school_id)
    else:
        # Handle the case where the user is not associated with any school
        school_offs = school_official.objects.none()
    # officialFilter = OfficialFilter(request.GET, queryset=officials)

    context = {
        "school_offs": school_offs,
    }

    return render(request, "officials/school_officials.html", context)


# # Athletes details......................................................
@login_required(login_url="login")
def DeleteAthlete(request, id):
    stud = Athlete.objects.get(id=id)
    if request.method == "POST":
        stud.delete()
        return redirect("athletes")

    return render(request, "dashboard/deleteath.html", {"obj": stud})


# # Athletes details......................................................
def OfficialDetail(request, id):
    official = get_object_or_404(school_official, id=id)
    relatedathletes = school_official.objects.filter(school=official.school).exclude(
        id=id
    )

    context = {
        "official": official,
        "relatedathletes": relatedathletes,
        # "breadcrumbs": breadcrumbs,
    }

    return render(request, "officials/official.html", context)



# Create your views here.




# schools list, tuple or array=====================================================================================
# @staff_required
from django.http import HttpResponse
import json
import uuid
import requests
from django.conf import settings
from django.http import JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.urls import reverse


logger = logging.getLogger(__name__)


def generate_unique_transaction_id():
    while True:
        transaction_id = str(random.randint(10**11, 10**12 - 1))
        if not Payment.objects.filter(transaction_id=transaction_id).exists():
            return transaction_id


def payment_view(request):
    user = request.user
    school = School.objects.get(user_id=user.id)

    if request.method == 'POST':
        form = PaymentForm(request.POST, school=school)
        if form.is_valid():
            try:
                phone_number = form.cleaned_data['phone_number']
                athletes = form.cleaned_data['athletes']

                if not athletes:
                    messages.error(request, "You must select at least one athlete.")
                    return render(request, 'payments/payment_form.html', {'form': form})

                total_amount = athletes.count() * 1500  # UGX 3,000 per athlete

                with transaction.atomic():  # Ensures atomicity in case of failure
                    payment = Payment.objects.create(
                        school=school,
                        amount=total_amount,
                        phone_number=phone_number,
                    )
                    payment.athletes.set(athletes)

                messages.success(request, f"Payment of UGX {total_amount} successful!")
                logger.info(f"Payment successful: School={school}, Amount={total_amount}, Phone={phone_number}")

                return redirect('payment', payment.id)

            except Exception as e:
                logger.error(f"Payment failed for {school}: {str(e)}", exc_info=True)
                messages.error(request, "An error occurred while processing the payment. Please try again.")

    else:
        form = PaymentForm(school=school)

    return render(request, 'payments/payment_form.html', {'form': form})



def get_airtel_token():
    """
    Retrieve Airtel Money OAuth token.
    """
    try:
        url = "https://openapi.airtel.africa/auth/oauth2/token"
        headers = {"Content-Type": "application/json", "Accept": "*/*" }
        payload = {
            "client_id": settings.AIRTEL_MONEY_CLIENT_ID,
            "client_secret": settings.AIRTEL_MONEY_CLIENT_SECRET,
            "grant_type": "client_credentials",
        }

        response = requests.post(url, json=payload, headers=headers, params={})
        logger.info(f"Token Response: {response.status_code}, {response.text}")
        print(response.json())
        if response.status_code == 200:
            return response.json().get("access_token")

        # Handle common errors
        error_response = response.json()
        error_message = error_response.get("error_description", error_response.get("message", "Unknown error"))

        if response.status_code == 400:
            logger.error("Invalid request format. Check parameters.")
            return None
        elif response.status_code == 401:
            logger.error("Authentication failed. Check your API credentials.")
            return None
        elif response.status_code == 403:
            logger.error("Permission denied. Your account may not have access.")
            return None
        elif response.status_code == 500:
            logger.error("Airtel Money server error. Try again later.")
            return None

        logger.error(f"Failed to get token: {error_message}")
        return None

    except requests.exceptions.ConnectionError:
        logger.error("Network error: Unable to reach Airtel Money API.")
        return None
    except requests.exceptions.Timeout:
        logger.error("Request timed out: Airtel Money API took too long to respond.")
        return None
    except requests.exceptions.RequestException as e:
        logger.error(f"Unexpected request error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unknown error: {str(e)}")
        return None

import random
from django.db import transaction as db_transaction

def generate_unique_transaction_id():
    """Generate a unique 12-digit transaction ID."""
    while True:
        transaction_id = str(random.randint(10**11, 10**12 - 1))  # 12-digit random number
        if not Payment.objects.filter(transaction_id=transaction_id).exists():  # Ensure uniqueness
            return transaction_id


def initiate_payment(request, id):
    payment = get_object_or_404(Payment, id=id)
    
    try:
        token = get_airtel_token()  
        if not token:
            return JsonResponse({"error": "Failed to get authentication token"}, status=500)

        payment_url = "https://openapi.airtel.africa/merchant/v2/payments/"
        transaction_id = generate_unique_transaction_id()  


        headers = {
            "Accept": "*/*",
            "Content-Type": "application/json",
            "X-Country": "UG",
            "X-Currency": "UGX",
            "Authorization": f"Bearer {token}",
            "x-signature": settings.AIRTEL_API_SIGNATURE,  # Ensure this is set in settings.py
            "x-key": settings.AIRTEL_API_KEY,  # Ensure this is set in settings.py
        }

        payload = {
            "reference": str(payment.transaction_id),  # Use the Payment ID as the reference
            "subscriber": {
                "country": "UG",
                "currency": "UGX",
                "msisdn": re.sub(r"\D", "", str(payment.phone_number)).lstrip('0'),   # Remove non-numeric characters
            },
            "transaction": {
                "amount": float(payment.amount),  # Convert DecimalField to float
                "country": "UG",
                "currency": "UGX",
                "id": transaction_id,  # Use the generated transaction ID
            }
        }

        response = requests.post(payment_url, json=payload, headers=headers)
        logger.info(f"Payment Response: {response.status_code}, {response.text}")

       # Update payment record with transaction ID and set status to PENDING
        with db_transaction.atomic():
            payment.transaction_id = transaction_id
            payment.status = "PENDING"  # Set status to pending until confirmed
            payment.save()

        if response.status_code == 200:
            return redirect(reverse('payment_success', args=[payment.transaction_id]))  # ✅ Redirect to success page
        else:
            return JsonResponse({"error": "Failed to initiate payment", "details": response.text}, status=400)

    except Exception as e:
        logger.error(f"Payment error: {str(e)}")
        return JsonResponse({"error": str(e)}, status=500)
   
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .models import Payment  # Use the Payment model

airtel_logger = logging.getLogger('airtel_callback')  # Use the specific logger

@csrf_exempt
def airtel_payment_callback(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed", status=405)

    try:
        # Log raw request body
        raw_body = request.body.decode('utf-8')
        airtel_logger.info(f"🔔 Airtel Callback Received: {raw_body}")

        # Parse JSON payload
        payload = json.loads(raw_body)
        airtel_logger.info(f"📜 Parsed JSON Payload:\n{json.dumps(payload, indent=2)}")

        # Extract transaction details
        transaction = payload.get("transaction", {})
        transaction_id = transaction.get("id")
        status_code = transaction.get("status_code")
        airtel_money_id = transaction.get("airtel_money_id")
        
        
        # Find the Payment record using transaction_id
        payment = get_object_or_404(Payment, transaction_id=transaction_id)

        # Map Airtel status to our system status
        status_mapping = {
            "TS": "COMPLETED",  # Transaction Successful
            "TF": "FAILED",      # Transaction Failed
            "TP": "PENDING",     # Transaction Pending
        }

        # Update payment status
        new_status = status_mapping.get(status_code, "FAILED")  # Default to FAILED if unknown status
        payment.status = new_status
        payment.save()

        airtel_logger.info(f"📌 Transaction ID: {transaction_id}, Status Code: {status_code}, Airtel Money ID: {airtel_money_id}")

        return JsonResponse({"message": "Callback received successfully"}, status=200)

    except json.JSONDecodeError:
        airtel_logger.error("❌ Invalid JSON received in callback")
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    except Exception as e:
        airtel_logger.error(f"❌ Error processing callback: {str(e)}")
        return JsonResponse({"error": "Internal Server Error"}, status=500)
    
    
# @csrf_exempt
# def airtel_payment_callback(request):

#     if request.method != 'POST':
#         return HttpResponse("Method Not Allowed", status=405)

#     try:
#         # Log the raw request body
#         raw_body = request.body.decode('utf-8')
#         logger.info(f"Raw Request Body: {raw_body}")

#         # Parse JSON payload
#         payload = json.loads(raw_body)
#         logger.info(f"Parsed JSON Payload: {json.dumps(payload, indent=2)}")

#         # Extract transaction details (corrected)
#         transaction = payload.get("transaction", {})  # Ensure transaction exists
#         transaction_id = transaction.get("id")  # Airtel's transaction ID
#         status_code = transaction.get("status_code")  # Example: "TS" (Success)
#         airtel_money_id = transaction.get("airtel_money_id")  # Airtel reference ID

#         logger.info(f"Transaction ID: {transaction_id}, Status Code: {status_code}, Airtel Money ID: {airtel_money_id}")

#         # Ensure required fields exist
#         if not all([transaction_id, status_code, airtel_money_id]):
#             logger.error("❌ Missing required fields in callback payload")
#             return JsonResponse({"error": "Invalid callback payload"}, status=400)

#         # Process the payment callback (Update Payment record)
#         return JsonResponse({"message": "Callback processed successfully"}, status=200)

#     except json.JSONDecodeError:
#         logger.error("❌ Invalid JSON payload received")
#         return JsonResponse({"error": "Invalid JSON"}, status=400)

#     except Exception as e:
#         logger.error(f"❌ Error processing callback: {str(e)}")
#         return JsonResponse({"error": "Internal Server Error"}, status=500)
    
    
    
def payment_success(request, transaction_id):
    payment = Payment.objects.filter(transaction_id=transaction_id).first()
    
    if not payment:
        return render(request, 'payment_failed.html', {'error': 'Transaction not found'})

    return render(request, 'payments/payment_success.html', {
        'amount': payment.amount,
        'transaction_id': payment.transaction_id,
        'timestamp': payment.created_at,  # Make sure your Payment model has `created_at`
    })
    
   
