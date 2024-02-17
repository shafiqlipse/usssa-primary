import django_filters
from .models import *
from django_select2.forms import Select2Widget


class OfficialFilter(django_filters.FilterSet):
    class Meta:
        model = school_official
        fields = ("name", "gender", "role", "email")


class schoolsFilter(django_filters.FilterSet):
    class Meta:
        model = School
        fields = ("school_name", "EMIS", "region", "district")



class AthleteFilter(django_filters.FilterSet):
    class Meta:
        model = Athlete
        fields = ("fname", "sport", "classroom", "gender")
        widgets = {
            "sport": Select2Widget,
        }


class AthletesFilter(django_filters.FilterSet):
    class Meta:
        model = Athlete
        fields = ("fname", "sport", "school", "gender")
        widgets = {
            "sport": Select2Widget,
            "school": Select2Widget,
            # "sport": Select2Widget,
        }
