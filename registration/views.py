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
