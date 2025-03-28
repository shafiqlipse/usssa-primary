from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

# from teams.views import delete_tdeam

urlpatterns = [

    path('pay/<int:id>/', initiate_payment, name='payment'),
    path('registration/', payment_view, name='registration'),
    path("calculate_age_choices/", calculate_age_choices, name="calculate_age_choices"),
    path("airtel-money/callback/", airtel_payment_callback, name="airtel_payment_callback"),
    path("get-athletes/", get_athletes, name="get-athletes"),
    path('payment/success/<str:transaction_id>/', payment_success, name='payment_success'),
    path('athletes/data/', athletes_data, name='athletes_data'),
    path('schools/data/', schools_data, name='schools_data'),
    # ===================School========================,
    path("deleteschool/<int:id>", DeleteSchool, name="delschool"),
    path("schools/", schools, name="schools"),
    path("school/", Dash, name="school_dashboard"),
    path("addschool/", Schoolnew, name="new_school"),
    path("school/<int:id>", school_detail, name="schooldetail"),
    path("editschool/<int:id>", school_update, name="schoolupdate"),
    
    # ===================Athletes========================,
    path("athletexs", athletexs, name="athletexs"),
    # path("athletes", athletes, name="athletes"),
    path("addathlete", newAthlete, name="addathlete"),
    path("athlete/<int:id>", AthleteDetail, name="athlete"),
    path("updateathlete/<int:id>", AthleteUpdate, name="updateathlete"),
    path("deleteathlete/<int:id>", DeleteAthlete, name="delathlete"),
    
   # ===================Officials========================,
    path("officials", school_offs, name="officials"),
    path("all_athletes/", all_athletes, name="athletex"),
    path("addofficial", Official, name="addofficial"),
    path("official/<int:id>", OfficialDetail, name="official"),
    path("all_officials/", all_officials, name="all_officials"),
       
   # ===================Officials========================,
    path("accounts/", accounts, name="accounts"),
    path("payments/", payments, name="payments"),
    path("pending_payments/", pending_payments, name="pending_payments"),
    path("activate_payment/<int:id>", activate_payment, name="activate_payment"),
    path("payment_detail/<int:id>", payment_detail, name="payment_detail"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
