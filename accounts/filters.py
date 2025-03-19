from django import forms
from .models import User  # Adjust according to your models
from dashboard.models import School  # Adjust according to your models

class UserFilterForm(forms.Form):
    username = forms.CharField(required=False, label="Username")
    email = forms.EmailField(required=False, label="Email")
    emis = forms.CharField(required=False, label="EMIS")

    def filter_queryset(self, queryset):
        if self.cleaned_data.get('username'):
            queryset = queryset.filter(username__icontains=self.cleaned_data['username'])
        if self.cleaned_data.get('email'):
            queryset = queryset.filter(email__icontains=self.cleaned_data['email'])
        if self.cleaned_data.get('emis'):
            queryset = queryset.filter(school_profile__first__EMIS__icontains=self.cleaned_data['emis'])
        return queryset
