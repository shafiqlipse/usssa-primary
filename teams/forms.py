from django import forms
from .models import *


class SchoolTeamForm(forms.ModelForm):
    athletes = forms.ModelMultipleChoiceField(
        queryset=Athlete.objects.all(), widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = SchoolTeam
        fields = [
            "sport",
            "gender",
            "championship",
            "age",
            "athletes",
        ]
        widgets = {
            "athletes": forms.CheckboxSelectMultiple,
        }
