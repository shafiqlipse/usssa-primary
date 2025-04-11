from django.db import models

# Create your models here.
from accounts.models import *
from core.models import *
from dashboard.models import *
# Create your models here.

class Team(models.Model):
    team_officer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    team_sport = models.ForeignKey(Sport, on_delete=models.CASCADE, null=True)
    team_age = models.ForeignKey(Age, on_delete=models.CASCADE, null=True)
    championship = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)

    team_gender = models.CharField(
        choices=[("Male", "male"), ("Female", "female")], max_length=10
    )
    def __str__(self):
        return str(self.team_officer)



class AthletesEnrollment(models.Model):
    team = models.ForeignKey(
        Team,
        related_name="team_athletes",  # Changed from "school_enrollments"
        on_delete=models.CASCADE,
    )
    athletes = models.ManyToManyField(Athlete)

    def save(self, *args, **kwargs):
        # Check for duplicates before saving
        if self.id:  # Only check if the instance already exists
            existing_athletes = set(self.athletes.values_list("id", flat=True))
            if len(existing_athletes) != self.athletes.count():
                raise ValidationError("An athlete cannot be added more than once.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.team.team_officer.district} - {self.team.team_sport}"