from django import forms
from dashboard.models import *
from core.models import *
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
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
            "district": Select2Widget,
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }


    def __init__(self, *args, **kwargs):
        super(OfficerForm, self).__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs["onchange"] = "displayImage(this);"


