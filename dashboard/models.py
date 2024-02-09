from django.db import models
from accounts.models import *
from datetime import date
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password

# Create your models here.
# Create your models here.


class School(models.Model):
    user = models.ForeignKey(
        User, related_name="school_profile", on_delete=models.CASCADE
    )
    school_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=19,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Active",
    )

    badge = models.ImageField(
        upload_to="badge/",
        blank=True,
        null=True,
    )
    EMIS = models.CharField(max_length=100, unique=True)
    center_number = models.CharField(max_length=100, null=True, blank=True, unique=True)

    region = models.ForeignKey(Region, related_name="region", on_delete=models.CASCADE)
    zone = models.ForeignKey(
        Zone,
        related_name="zone",
        on_delete=models.CASCADE,
    )


class school_official(models.Model):
    school = models.ForeignKey(
        School, related_name="school", on_delete=models.CASCADE
    )
    
    name = models.CharField(max_length=100, null=True, blank=True, default="")
    email = models.EmailField(null=True, blank=True, default="")
    phone_number = models.CharField(max_length=15, null=True, blank=True, default="")
    nin = models.CharField(max_length=20, default="")
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female")],
        null=True,
        blank=True,
    )
    role = models.CharField(
        max_length=10,
        choices=[("Manager", "Manager"), ("Medical", "Medical"), ("Coach", "Coach")],
        null=True,
        blank=True,
    )

    photo = models.ImageField(
        upload_to="badge/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name


class Classroom(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Age(models.Model):
    name = models.CharField(max_length=255)
    min_age = models.IntegerField(blank=True, null=True)
    max_age = models.IntegerField(blank=True, null=True)

    def clean(self):
        if (
            self.min_age is not None
            and self.max_age is not None
            and self.min_age > self.max_age
        ):
            raise ValidationError(
                "Minimum age must be less than or equal to maximum age."
            )

    def __str__(self):
        return self.name


class AthleteManager(models.Manager):
    def get_queryset(self):
        today = date.today()
        queryset = super().get_queryset()
        queryset = queryset.filter(date_of_birth__lte=today)
        return queryset.annotate(
            calculated_age=models.ExpressionWrapper(
                today.year - models.F("date_of_birth__year"),
                output_field=models.IntegerField(),
            )
        )

    def filter_by_age_range(self, min_age, max_age):
        return self.get_queryset().filter(
            calculated_age__gte=min_age, calculated_age__lte=max_age
        )


class Athlete(models.Model):
    name = models.CharField(max_length=255)
    lin = models.IntegerField()
    sport = models.ForeignKey(Sport, related_name="sport", on_delete=models.CASCADE)
    school = models.ForeignKey(School, related_name="schooler", on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(
        choices=[("Male", "male"), ("Female", "female")], max_length=10
    )
    classroom = models.ForeignKey(
        Classroom, related_name="classroom", on_delete=models.CASCADE
    )

    photo = models.ImageField(upload_to="athlete_photos/", blank=True, null=True)

    Parent_guadian = models.CharField(max_length=100, null=True, blank=True, default="")
    parent_email = models.EmailField(null=True, blank=True, default="")
    parent_phone_number = models.CharField(
        max_length=15, null=True, blank=True, default=""
    )
    parent_nin = models.CharField(max_length=20, null=True, blank=True, default="")
    address = models.CharField(max_length=20, null=True, blank=True, default="")
    parent_gender = models.CharField(
        max_length=10,
        choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        null=True,
        blank=True,
    )

    relationship = models.CharField(
        max_length=10,
        choices=[("Father", "Father"), ("Mother", "Mother"), ("Guardian", "Guardian")],
        null=True,
        blank=True,
    )
    objects = AthleteManager()

    def save(self, *args, **kwargs):
        # Find the corresponding age range and assign it to the athlete
        age = date.today().year - self.date_of_birth.year
        age_range = Age.objects.filter(min_age__lte=age, max_age__gte=age).first()
        self.age = age_range

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
