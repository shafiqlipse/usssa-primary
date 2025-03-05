from django import forms
from accounts.models import *
from school.models import *

class PaymentForm(forms.Form):
    phone_number = forms.CharField(
        label="Phone Number",
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Enter phone number'})
    )
    athletes = forms.ModelMultipleChoiceField(
        queryset=Athlete.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if school:
            # Fetch only unpaid learners in the specific class
            self.fields['athletes'].queryset = Athlete.objects.filter(
                school=school, status='NEW'
            )
            # Customize labels to include the amount for each learner
            self.fields['athletes'].label_from_instance = lambda obj: f"{obj.fname} (Amount: 1500)"