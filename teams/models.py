from django.db import models
from accounts.models import *
from core.models import *
from dashboard.models import *

# Create your models here.


class SchoolTeam(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, null=True)
    championship = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)
    age = models.ForeignKey(Age, on_delete=models.CASCADE, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "male"), ("Female", "female")],
    )
    status = models.CharField(
        max_length=10,
        default="Inactive",
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        null=True,
    )
    athletes = models.ManyToManyField(Athlete)

    def __str__(self):
        return str(self.school)
