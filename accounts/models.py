from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


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


class User(AbstractUser):
    is_school = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to="profile/", blank=True, null=True)




class Tournament(models.Model):
    name = models.CharField(max_length=245)
    host = models.CharField(max_length=245)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to="champImages/", blank=True, null=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField(max_length=245)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name




class TOfficer(models.Model):
    user = models.ForeignKey(
        User, related_name="tuser", on_delete=models.CASCADE, null=True
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

