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


class Zone(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

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
    
