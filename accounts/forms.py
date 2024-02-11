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
        fields = [
            "school_name",
            "EMIS",
            "center_number",
            "badge",
            "region",
            "district",
            "county",
            "subcounty",
        ]

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
            "fname",
            "mname",
            "lname",
            "lin",
            "sport",
            "date_of_birth",
            "gender",
            "classroom",
            "photo",
            "Parent_fname",
            "Parent_lname",
            "parent_phone_number",
            "parent_nin",
            "address",
            "relationship",
            "designation",
            "status",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

        def clean_date_of_birth(self):
            date_of_birth = self.cleaned_data.get("date_of_birth")
            age = date.today().year - date_of_birth.year

            if not (9 <= age <= 14):
                raise forms.ValidationError(
                    "Athlete must be between 9 and 14 years old."
                )

            return date_of_birth
