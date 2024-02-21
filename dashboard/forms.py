# forms.py
from django import forms
from .models import Athlete

class AthleteSelectionForm(forms.Form):
    athletes = forms.ModelMultipleChoiceField(
        queryset=Athlete.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )
