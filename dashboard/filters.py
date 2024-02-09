import django_filters
from .models import *


class OfficialFilter(django_filters.FilterSet):
    class Meta:
        model = school_official
        fields = ("name", "gender", "role","email")


class schoolsFilter(django_filters.FilterSet):
    class Meta:
        model = School
        fields = ("school_name", "EMIS", "zone", "region")


class AthleteFilter(django_filters.FilterSet):
    class Meta:
        model = Athlete
        fields = ("name", "sport", "classroom", "gender")
