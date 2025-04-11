from django.db import models
from accounts.models import *
from dashboard.models import Athlete, Age

# Create your models here.


class Officer(models.Model):
    user = models.ForeignKey(
        User, related_name="officer_profile", on_delete=models.CASCADE, null=True
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
    city = models.ForeignKey(
        District,
        related_name="cito",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    region = models.ForeignKey(
        Region,
        related_name="regiono",
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


