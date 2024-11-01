from django.db import models
from accounts.models import District

# Create your models here.


class Teacher(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    photo = models.ImageField(
        upload_to="photo/",
    )

    district = models.ForeignKey(
        District,
        related_name="districtt",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    contact = models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )
    school = models.CharField(max_length=125)

    gender = models.CharField(
        max_length=14,
        choices=[("Male", "Male"), ("Female", "Female")],
    )
    designation = models.CharField(
        max_length=40,
        choices=[
            ("Principal", "Principal"),
            ("HeadTeacher", "HeadTeacher"),
            ("Deputy HeadTeacher", "Deputy HeadTeacher"),
        ],
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.fname
