from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.core import exceptions as django_exceptions
from django_filters.filters import OrderingFilter
from rest_framework.serializers import ValidationError

from wingz.restframework.filters import BaseFilterSet, CoordinateFilter

from ..models import Ride


class RideOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra["choices"] += [
            ("distance_to_pickup", "Distance to pickup location"),
            ("-distance_to_pickup", "Distance to pickup location (descending)"),
        ]

    def filter(self, queryset, value):
        try:
            qs = super().filter(queryset, value)
        except django_exceptions.FieldError:
            if any(v in ["distance_to_pickup", "-distance_to_pickup"] for v in value):
                raise ValidationError(
                    "gps_location is required when sort by distance_to_pickup"
                )
            return queryset
        return qs


class RideFilter(BaseFilterSet):
    gps_location = CoordinateFilter(
        method="filter_by_gps_location",
        label="Pickup GPS location, used when sort by the distance to this location",
    )
    ordering = RideOrderingFilter(fields=[("pickup_time1", "pickup_time")])

    class Meta:
        model = Ride
        fields = {
            "status": ["exact"],
            "rider__email": ["exact", "icontains"],
        }
        field_labels = {
            "status": "Ride status filter",
            "rider__email": "Rider email exact filter",
            "rider__email__icontains": "Rider email fuzzy query filter, ignore case",
        }

    def filter_by_gps_location(self, qs, _, value):
        lat, lon = self.validate_gps_location(value)
        gps_location = Point(lat, lon, srid=4326)
        qs = qs.annotate(distance_to_pickup=Distance("pickup_pos", gps_location))
        return qs

    def validate_gps_location(self, value):
        if not value or len(value) != 2:
            raise ValidationError(
                "Please provide exactly two parameters: latitude and longitude."
            )
        lat, lon = value
        try:
            lat, lon = float(lat), float(lon)
        except ValueError:
            raise ValidationError("Latitude and longitude must be valid numbers.")

        if not (-90 <= lat <= 90):
            raise ValidationError("Latitude must be between -90 and 90.")
        if not (-180 <= lon <= 180):
            raise ValidationError("Longitude must be between -180 and 180.")
        return lat, lon
