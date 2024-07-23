from django.db import models


class Swimmer(models.Model):

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    photo = models.ImageField(
        upload_to="photo/",
    )

    date_of_birth = models.DateField()

    school = models.CharField(max_length=125)

    gender = models.CharField(
        max_length=14,
        choices=[("Male", "Male"), ("Female", "Female")],
    )
    category = models.CharField(
        max_length=40,
        choices=[
            ("Swimming Boys", "Swimming Boys"),
            ("Swimming Girls", "Swimming Girls"),
        ],
    )
    classroom = models.CharField(
        max_length=40,
        choices=[
            ("S1", "S1"),
            ("S2", "S2"),
            ("S3", "S3"),
            ("S4", "S4"),
            ("S5", "S5"),
            ("S6", "S6"),
        ],
    )


def __str__(self):
    return f"{self.first_name} {self.last_name}"
