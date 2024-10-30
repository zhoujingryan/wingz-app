from wingz.restframework.filters import BaseFilterSet

from ..models import Ride


class RideFilter(BaseFilterSet):

    class Meta:
        model = Ride
        fields = {
            "status": ["exact"],
            "rider__email": ["exact", "icontains"],
        }
        field_labels = {
            "status": "ride status filter",
            "rider__email": "rider email exact filter",
            "rider__email__icontains": "rider email fuzzy query filter, ignore case",
        }
