from django.db import models
from dashboard.models import School, Athlete
# Create your models here.
import random
import string
   
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