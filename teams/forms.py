from django import forms
from .models import *


class SchoolTeamForm(forms.ModelForm):
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
