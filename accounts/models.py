from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

class User(AbstractUser):
    is_school = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="profile/", blank=True, null=True)
    date_joined = models.DateTimeField(default=now)  # Use timezone.now()




class Sport(models.Model):
    name = models.CharField(max_length=245)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Municipality(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Tournament(models.Model):
    name = models.CharField(max_length=245)
    host = models.CharField(max_length=245)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="champImages/", blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[("Active", "Active"), ("Inactive", "Inactive")], blank=True, null=True
    )
    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name

