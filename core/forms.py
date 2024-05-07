from django import forms
from dashboard.models import *
from core.models import *
from django_select2.forms import Select2Widget


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["team_gender", "team_sport", "athletes"]

        widgets = {
            "athletes": forms.CheckboxSelectMultiple(),
        }


class OfficerForm(forms.ModelForm):
    class Meta:
        model = Officer
        fields = [
            "first_name",
            "last_name",
            "nin",
            "photo",
            "phone_number",
            "email",
            "gender",
            "date_of_birth",
            "region",
            "district",
            "status",
        ]

        widgets = {
            "district": Select2Widget,
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(OfficerForm, self).__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs["onchange"] = "displayImage(this);"


class TOfficerForm(forms.ModelForm):
    class Meta:
        model = TOfficer
        fields = [
            "first_name",
            "last_name",
            "nin",
            "photo",
            "phone_number",
            "email",
            "gender",
            "date_of_birth",
            "role",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(OfficerForm, self).__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs["onchange"] = "displayImage(this);"
