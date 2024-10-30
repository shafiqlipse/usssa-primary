from django import forms
from dashboard.models import *
from accounts.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django_select2.forms import Select2Widget


class SchoolRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "phone",
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
            "fname",
            "lname",
            "nin",
            "photo",
            "phone_number",
            "email",
            "gender",
            "date_of_birth",
            "gfname",
            "glname",
            "gnin",
            "gphoto",
            "gphone",
            "gemail",
            "ggender",
            "gdate_of_birth",
        ]

        widgets = {
            # "badge": ImageCropWidget,
            # "photo": ImageCropWidget,
            # "gphoto": ImageCropWidget,
            "school_name": forms.TextInput(attrs={"class": "form-control"}),
            "EMIS": forms.TextInput(attrs={"class": "form-control"}),
            "center_number": forms.TextInput(attrs={"class": "form-control"}),
            "region": forms.Select(attrs={"class": "form-control"}),
            "district": forms.Select(attrs={"class": "form-control"}),
            #    --------------------------------------
            "fname": forms.TextInput(attrs={"class": "form-control"}),
            "lname": forms.TextInput(attrs={"class": "form-control"}),
            "nin": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            #    --------------------------------------
            "gfname": forms.TextInput(attrs={"class": "form-control"}),
            "glname": forms.TextInput(attrs={"class": "form-control"}),
            "gnin": forms.TextInput(attrs={"class": "form-control"}),
            "gphone_number": forms.TextInput(attrs={"class": "form-control"}),
            "gemail": forms.TextInput(attrs={"class": "form-control"}),
            "ggender": forms.Select(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "gdate_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super(SchoolProfileForm, self).__init__(*args, **kwargs)
        self.fields["badge"].widget.attrs["onchange"] = "displayImage(this);"

    def __init__(self, *args, **kwargs):
        super(SchoolProfileForm, self).__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs["onchange"] = "displayImage(this);"

    def __init__(self, *args, **kwargs):
        super(SchoolProfileForm, self).__init__(*args, **kwargs)
        self.fields["gphoto"].widget.attrs["onchange"] = "displayImage(this);"


class SchoolEditForm(forms.ModelForm):
    class Meta:
        model = School
        fields = [
            "school_name",
            "EMIS",
            "center_number",
            "badge",
            "region",
            "district",
            "fname",
            "lname",
            "nin",
            "photo",
            "phone_number",
            "email",
            "gender",
            "date_of_birth",
            "gfname",
            "glname",
            "gnin",
            "gphoto",
            "gphone",
            "gemail",
            "ggender",
            "gdate_of_birth",
            "status",
        ]

        widgets = {
            "district": Select2Widget,
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
            "gdate_of_birth": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super(SchoolProfileForm, self).__init__(*args, **kwargs)
        self.fields["badge"].widget.attrs["onchange"] = "displayImage(this);"

    def __init__(self, *args, **kwargs):
        super(SchoolProfileForm, self).__init__(*args, **kwargs)
        self.fields["photo"].widget.attrs["onchange"] = "displayImage(this);"

    def __init__(self, *args, **kwargs):
        super(SchoolProfileForm, self).__init__(*args, **kwargs)
        self.fields["gphoto"].widget.attrs["onchange"] = "displayImage(this);"


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
            # "photo": ImageCropWidget,
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "fname": forms.TextInput(attrs={"class": "form-control"}),
            "lname": forms.TextInput(attrs={"class": "form-control"}),
            "nin": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.TextInput(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "role": forms.Select(attrs={"class": "form-control"}),
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
            "age",
            "photo",
            "Parent_fname",
            "designation",
            "Parent_lname",
            "parent_phone_number",
            "parent_nin",
            "address",
            "relationship",
        ]
        widgets = {
            #    --------------------------------------
            "fname": forms.TextInput(attrs={"class": "form-control"}),
            "mname": forms.TextInput(attrs={"class": "form-control"}),
            "lname": forms.TextInput(attrs={"class": "form-control"}),
            "lin": forms.TextInput(attrs={"class": "form-control"}),
            "Parent_fname": forms.TextInput(attrs={"class": "form-control"}),
            "Parent_lname": forms.TextInput(attrs={"class": "form-control"}),
            "parent_phone_number": forms.TextInput(attrs={"class": "form-control"}),
            "parent_nin": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "designation": forms.TextInput(attrs={"class": "form-control"}),
            "sport": forms.Select(attrs={"class": "form-control"}),
            "age": forms.Select(attrs={"class": "form-control"}),
            "classroom": forms.Select(attrs={"class": "form-control"}),
            "gender": forms.Select(attrs={"class": "form-control"}),
            "relationship": forms.Select(attrs={"class": "form-control"}),
            "date_of_birth": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
        }


class UpdateAthleteForm(forms.ModelForm):
    class Meta:
        model = Athlete
        fields = [
            "fname",
            "mname",
            "lname",
            "sport",
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
        ]
