from django import forms
from dashboard.models import *
from .models import *


class SchoolEnrollmentForm(forms.ModelForm):
    class Meta:
        model = SchoolEnrollment
        fields = [
            "championship",
            "sport","age","status","gender",
        ]
        widgets = {
            "championship": forms.Select(attrs={"class": "form-control"}),
            "sport": forms.Select(attrs={"class": "form-control"}),
            "age": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
        }


class AthleteEnrollmentForm(forms.ModelForm):
    athletes = forms.ModelMultipleChoiceField(
        queryset=Athlete.objects.filter(status="ACTIVE"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = AthleteEnrollment
        fields = ["athletes"]
