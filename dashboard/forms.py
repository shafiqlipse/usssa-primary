# forms.py
from django import forms
from .models import Athlete

class AthleteSelectionForm(forms.Form):
    athletes = forms.ModelMultipleChoiceField(
        queryset=Athlete.objects.filter(status = 'Active'),
        widget=forms.CheckboxSelectMultiple,
    )
