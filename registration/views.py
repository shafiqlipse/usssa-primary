from django.shortcuts import render

# # Create your views here.
#     #Main
#     x_country = "country_code?"
#     x_currency = "currency_code?"
#     #Check if sandbox or production
#     #Choose either sandbox or production
#     environment_mode = "stagging"
#     #pin
#     disbursement_pin = "your disbursement pin?"

#     #Configure keys
#     client_id = "client_id?"
#     client_secret = "client_secret?"

# # payload
# from classes.airtel_pay import AirtelPay

# #Request pay
# pay = AirtelPay.pay("ten_digits_phone_number", "amount", "currency_code", "country_code", "transaction_id")
# print(pay["jsondata"])

# from classes.airtel_pay import AirtelPay

# #Disburse funds
# transfer = AirtelPay.transfermoney("airtel_phone_number", "amount")
# print(transfer)


def registration(request):
    context = {}
    return render(request, "", context)


# views.py

from accounts.models import *
from dashboard.models import *
from django.shortcuts import render, redirect
from .models import Enrollment
from .forms import AthleteSelectionForm


def competition_list(request):
    tournaments = Tournament.objects.all()
    return render(request, "tourns.html", {"tournaments": tournaments})


def enroll_school(request, id):
    tournament = Tournament.objects.get(id=id)
    school = (
        request.user.school_profile.first()
    )  # Assuming you have a way to get the user's school

    if request.method == "POST":
        # Form submission
        form = AthleteSelectionForm(request.POST)
        if form.is_valid():
            athlete_ids = form.cleaned_data["athletes"]
            enrollment = Enrollment.objects.create(tournament=tournament, school=school)
            enrollment.athletes.add(*athlete_ids)
            return redirect("tourns")
    else:
        # Display the form
        form = AthleteSelectionForm()
        # Filter athletes belonging to the user's school
        form.fields["athletes"].queryset = Athlete.objects.filter(school=school)

    return render(
        request, "reg/enroll_school.html", {"form": form, "tournament": tournament}
    )


# The view to display athletes and handle selection will be similar to the above enroll_school view
