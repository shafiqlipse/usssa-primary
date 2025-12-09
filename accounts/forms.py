

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserEditForm(forms.ModelForm):
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password', 'class': 'form-control'}),
        label="New Password"
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password', 'class': 'form-control'}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.password = make_password(new_password)
        if commit:
            user.save()
        return user
