


from django.db import models
from django.utils import timezone
from accounts.models import *
from dashboard.models import *

class Enrollment(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    school = models.ForeignKey(School, related_name='enrollments', on_delete=models.CASCADE)
    athletes = models.ManyToManyField(Athlete, related_name='enrollments')
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Enrollment ID: {self.id} - Competition: {self.competition}"
