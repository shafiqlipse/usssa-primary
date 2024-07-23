import django_filters
from .models import Swimmer


class swimmerFilter(django_filters.FilterSet):

    # Add more fields as needed

    class Meta:
        model = Swimmer
        fields = [
            "first_name",
            "last_name",
            "category",
            "school",
            "gender",
        ]  # Add all fields you want to filter on
