from django.db import models
from dashboard.models import School, Athlete
# Create your models here.
from django.core.exceptions import ValidationError
import re

class Payment(models.Model):

        transaction_id = models.CharField(max_length=100,null=True, blank=True)
        amount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
     
        phone_number = models.CharField(max_length=15)
        status = models.CharField(
        max_length=20, 
        choices=[('PENDING', 'PENDING'), ('COMPLETED', 'COMPLETED')], 
        default='PENDING'
    )
  
        created_at = models.DateTimeField(auto_now_add=True)
        school = models.ForeignKey(School, on_delete=models.CASCADE)
        athletes = models.ManyToManyField(Athlete, related_name='payments')
        
        def __str__(self):
            return f"{self.transaction_id} - {self.amount} {self.school}"
            
                
        def clean(self):
            """Validate phone number format."""
            if not re.match(r'^(075|074|070)\d{7}$', self.phone_number):
                raise ValidationError("Phone number must a valid Airtel money number.")

        def save(self, *args, **kwargs):
            """Ensure validation before saving."""
            self.clean()
            super().save(*args, **kwargs)