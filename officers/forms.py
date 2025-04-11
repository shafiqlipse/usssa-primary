from django import forms
from .models import *

from django import forms
from dashboard.models import *
from .models import *


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = [
            "championship",
            "team_sport","team_age","team_gender",
        ]
        widgets = {
            "championship": forms.Select(attrs={"class": "form-control"}),
            "team_sport": forms.Select(attrs={"class": "form-control"}),
            "team_age": forms.Select(attrs={"class": "form-control"}),
            "team_gender": forms.Select(attrs={"class": "form-control"}),
        }


class AthleteEnrollmentForm(forms.ModelForm):
    athletes = forms.ModelMultipleChoiceField(
        queryset=Athlete.objects.filter(status="ACTIVE"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = AthletesEnrollment
        fields = ["athletes"]

