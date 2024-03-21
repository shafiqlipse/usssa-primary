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
        User, related_name="school_profile", on_delete=models.CASCADE, null=True
    )
    school_name = models.CharField(max_length=100)
    status = models.CharField(
        max_length=19,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        default="Inactive",
    )
    badge = models.ImageField(
        upload_to="badge/",
        blank=True,
        null=True,
    )
    EMIS = models.CharField(max_length=100, unique=True)
    center_number = models.CharField(max_length=100, null=True, blank=True, unique=True)
    district = models.ForeignKey(
        District,
        related_name="district",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    region = models.ForeignKey(
        Region,
        related_name="region",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    municipality = models.ForeignKey(
        Municipality,
        related_name="county",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    city = models.ForeignKey(
        City,
        related_name="subcounty",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # headteacher
    lname = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    nin = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female")],
    )
    photo = models.ImageField(
        upload_to="badge/",
        blank=True,
        null=True,
    )

    # games teacher
    gfname = models.CharField(max_length=100, null=True, blank=True, default="")
    glname = models.CharField(max_length=100, null=True, blank=True, default="")
    gemail = models.EmailField(null=True, blank=True, default="")
    gphone = models.CharField(max_length=15, null=True, blank=True, default="")
    gnin = models.CharField(max_length=20, default="")
    gdate_of_birth = models.DateField()
    ggender = models.CharField(
        max_length=1,
        choices=[("M", "Male"), ("F", "Female")],
        null=True,
        blank=True,
    )
    gphoto = models.ImageField(
        upload_to="badge/",
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.school_name


class school_official(models.Model):
    school = models.ForeignKey(School, related_name="school", on_delete=models.CASCADE)
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
        max_length=40,
        choices=[
            ("Coach", "Coach"),
            ("Teacher", "Teacher"),
            ("Assistant Games Teacher", "Assistant Games Teacher"),
            ("Assistant Head Teacher", "Assistant Head Teacher"),
            ("Nurse", "Nurse"),
            ("Doctor", "Doctor"),
            ("District Education Officer", "District Education Officer"),
            ("District Sports Officer", "District Sports Officer"),
        ],
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


from PIL import Image


class Athlete(models.Model):
    fname = models.CharField(max_length=255)
    mname = models.CharField(
        max_length=255,
        null=True,
        blank=True,
    )
    lname = models.CharField(max_length=255)
    lin = models.CharField(max_length=255, unique=True)

    sport = models.ForeignKey(Sport, related_name="sport", on_delete=models.CASCADE)
    school = models.ForeignKey(
        School, related_name="schooler", on_delete=models.CASCADE
    )
    date_of_birth = models.DateField()
    gender = models.CharField(
        choices=[("Male", "male"), ("Female", "female")], max_length=10
    )
    classroom = models.ForeignKey(
        Classroom, related_name="classroom", on_delete=models.CASCADE
    )
    age = models.ForeignKey(Age, related_name="age", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="athlete_photos/")

    Parent_fname = models.CharField(max_length=100)
    Parent_lname = models.CharField(max_length=100)
    parent_phone_number = models.CharField(max_length=15)
    parent_nin = models.CharField(max_length=20)
    address = models.CharField(max_length=20)
    designation = models.CharField(max_length=20)
    relationship = models.CharField(
        max_length=15,
        choices=[("Father", "Father"), ("Mother", "Mother"), ("Other", "Other")],
        null=True,
        blank=True,
    )
    # New field to track payment status

    status = models.CharField(
        max_length=10,
        choices=[("Active", "Active"), ("Inactive", "Inactive")],
        null=True,
        blank=True,
        default="Active",
    )
    objects = AthleteManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Open the uploaded image
        img = Image.open(self.photo.path)

        # Set the maximum size you want for the image
        max_size = (300, 300)

        # Resize the image
        img.thumbnail(max_size)

        # Save the resized image back to the same path
        img.save(self.photo.path)

    def save(self, *args, **kwargs):
        # Find the corresponding age range and assign it to the athlete
        age = date.today().year - self.date_of_birth.year
        age_range = Age.objects.filter(min_age__lte=age, max_age__gte=age).first()
        self.age = age_range

        super().save(*args, **kwargs)

    def __str__(self):
        return self.fname


class Payment(models.Model):
    athletes = models.ManyToManyField(Athlete)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_paid = models.BooleanField(default=False)
