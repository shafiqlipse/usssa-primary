from django import forms
from dashboard.models import *
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm


class SchoolRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            "email",
            "username",
            "password1",
            "password2",
            "is_school",
        ]


class SchoolProfileForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ["school_name", "EMIS", "center_number", "badge", "region", "zone"]

    def __init__(self, *args, **kwargs):
        super(SchoolProfileForm, self).__init__(*args, **kwargs)
        self.fields["badge"].widget.attrs["onchange"] = "displayImage(this);"


class OfficialForm(forms.ModelForm):
    class Meta:
        model = school_official
        fields = [
            "name",
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
        super(OfficialForm, self).__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs["onchange"] = "displayImage(this);"


class NewAthleteForm(forms.ModelForm):
    class Meta:
        model = Athlete
        fields = [
            "name",
            "lin",
            "sport",
            "date_of_birth",
            "gender",
            "classroom",
          
            "photo",
            "Parent_guadian",
            "parent_email",
            "parent_phone_number",
            "parent_nin",
            "parent_gender",
            "address",
        ]