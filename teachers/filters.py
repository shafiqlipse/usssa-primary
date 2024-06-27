import django_filters
from .models import Teacher


class TeacherFilter(django_filters.FilterSet):

    # Add more fields as needed

    class Meta:
        model = Teacher
        fields = [
            "first_name",
            "district",
            "school",
            "designation",
            "gender",
        ]  # Add all fields you want to filter on
