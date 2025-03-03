from django import forms
from dashboard.models import *
from core.models import *
from django_select2.forms import Select2Widget


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ["team_gender", "team_age", "team_sport", "athletes", "championship"]
        widgets = {
            "team_gender": forms.Select(attrs={"class": "form-select"}),
            "team_age": forms.Select(attrs={"class": "form-select"}),
            "team_sport": forms.Select(attrs={"class": "form-select"}),
            "athletes": forms.SelectMultiple(
                attrs={"class": "form-select js-example-basic-multiple", "multiple": "multiple"}
            ),
            "championship": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields["athletes"].widget.attrs.update({"class": "js-example-basic-multiple"})


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
            "district",
            "gender",
            "role",
        ]

        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(TOfficerForm, self).__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs["onchange"] = "displayImage(this);"
