from django import forms
from .models import *
from django_select2.forms import Select2Widget



class SportsOfficerForm(forms.ModelForm):
    class Meta:
        model = SportsOfficer
        fields = [
            "first_name",
            "last_name",
            "nin",
            "photo",
            "phone_number",
            "email",
            "gender",
            "date_of_birth",
            "district",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "nin": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date","class": "form-control"}),
          
            "district": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super(SportsOfficerForm, self).__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs["onchange"] = "displayImage(this);"


class TOfficerForm(forms.ModelForm):
    class Meta:
        model = TeamOfficer
        fields = [
            "first_name",
            "last_name",
            "nin",
            "photo",
            "phone_number",
            "district",
            "gender",
            "role",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "nin": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date","class": "form-control"}),
            "role": forms.TextInput(attrs={"class": "form-control"}),
            "district": forms.TextInput(attrs={"class": "form-form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super(TOfficerForm, self).__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs["onchange"] = "displayImage(this);"



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

