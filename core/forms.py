from django import forms
from dashboard.models import *
from core.models import *
from django_select2.forms import Select2Widget



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
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "nin": forms.TextInput(attrs={"class": "form-control"}),
            "photo": forms.FileInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "date_of_birth": forms.DateInput(attrs={"type": "date","class": "form-control"}),
            "region": forms.Select(attrs={"class": "form-select"}),
            "district": forms.Select(attrs={"class": "form-select"}),
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
