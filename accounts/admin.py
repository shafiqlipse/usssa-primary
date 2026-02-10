from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import *
from school.models import *

class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "is_active", "is_school", "is_staff", "is_admin")  # Columns to display
    search_fields = ("username", "email")  # Enables search
    list_filter = ("is_active", "is_school", "is_staff", "is_admin", )  # Enables filtering

class AthleteAdmin(admin.ModelAdmin):  # Inherit from admin.ModelAdmin
    list_display = ("fname", "lname", "lin", "gender", "classroom", "school", "date_of_birth")
    search_fields = ("fname", "lname", "lin", "school__school_name")  # Use school__name instead of school
    list_filter = ("classroom", "gender")
# Register your models here.
# admin.site.register(Athlete, AthleteAdmin) 

class SchoolAdmin(admin.ModelAdmin):  # Inherit from admin.ModelAdmin
    list_display = ("school_name", "center_number", "EMIS", "district")
    search_fields =( "school_name", "center_number", "EMIS")  # Use school__name instead of school

# Register your models here.
admin.site.register(User, UserAdmin)
# admin.site.register(Age)
admin.site.register(Sport)
admin.site.register(Tournament)
admin.site.register(Region)
admin.site.register(District)
admin.site.register(School,SchoolAdmin)
admin.site.register(Athlete,AthleteAdmin)
admin.site.register(City)
admin.site.register(Municipality)
# admin.site.register(Classroom)
# admin.site.register(TOfficer)
admin.site.register(school_official)
