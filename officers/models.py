from django.db import models

# Create your models here.
from school.models import *
from accounts.models import *
# Create your models here.



class SportsOfficer(models.Model):
    user = models.ForeignKey(
        User, related_name="sports_officer", on_delete=models.CASCADE, null=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=19,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Inactive",
        null=True,
        blank=True,
    )
    photo = models.ImageField(
        upload_to="photo/",
    )

    district = models.ForeignKey(
        District,
        related_name="districto",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    nin = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female")],
    )

    def __str__(self):
        return self.email






class TeamOfficer(models.Model):
    user = models.ForeignKey(
        User, related_name="team_user", on_delete=models.CASCADE, null=True
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    photo = models.ImageField(
        upload_to="photo/",
    )
   
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=25)
    district = models.CharField(max_length=25, null=True, blank=True)
    nin = models.CharField(max_length=20, unique=True)
  
    gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female")],
    )

    def __str__(self):
        return self.first_name











class Team(models.Model):
    team_officer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    team_sport = models.ForeignKey(Sport, on_delete=models.CASCADE, null=True)
    team_age = models.ForeignKey(Age, on_delete=models.CASCADE, null=True)
    championship = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)

    team_gender = models.CharField(
        choices=[("Male", "male"), ("Female", "female")], max_length=10
    )
    
    class Meta:
        unique_together = ("team_sport", "championship", "team_age", "team_gender")
        
        
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