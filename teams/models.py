from django.db import models
from accounts.models import *
from core.models import *
from dashboard.models import *

# Create your models here.


# Create your models here.
class SchoolEnrollment(models.Model):
    school = models.ForeignKey(
        School, related_name="enrollments", on_delete=models.CASCADE
    )
    championship = models.ForeignKey(
        Tournament, related_name="school_enrollments", on_delete=models.CASCADE
    )
    sport = models.ForeignKey(
        Sport, related_name="athlete_enrollments", on_delete=models.CASCADE
    )
    enrollment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.school.school_name} - {self.championship.name}"


class AthleteEnrollment(models.Model):
    school_enrollment = models.ForeignKey(
        SchoolEnrollment,
        related_name="athlete_enrollments",  # Changed from "school_enrollments"
        on_delete=models.CASCADE,
    )
    athletes = models.ManyToManyField(Athlete)

    def save(self, *args, **kwargs):
        # Check for duplicates before saving
        if self.pk:  # Only check if the instance already exists
            existing_athletes = set(self.athletes.values_list("id", flat=True))
            if len(existing_athletes) != self.athletes.count():
                raise ValidationError("An athlete cannot be added more than once.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.school_enrollment.school.school_name} - {self.school_enrollment.sport.name}"