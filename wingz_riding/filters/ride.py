from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.core import exceptions as django_exceptions
from django_filters import filters
from django_filters.filters import OrderingFilter
from rest_framework.serializers import ValidationError

from wingz.restframework.filters import BaseFilterSet, CoordinateFilter

from ..models import Ride


class RideOrderingFilter(OrderingFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra["choices"] += [
            ("distance_to_pickup", "Distance to pickup location"),
        ]

    def filter(self, queryset, value):
        try:
            qs = super().filter(queryset, value)
        except django_exceptions.FieldError:
            if "distance_to_pickup" in value:
                raise ValidationError(
                    "gps_location is required when sort by distance_to_pickup"
                )
            # never
            return queryset  # pragma: no cover
        return qs


class RideFilter(BaseFilterSet):
    gps_location = CoordinateFilter(
        method="filter_by_gps_location",
        label="Pickup GPS location, used when sort by the distance to this location",
    )
    ordering = RideOrderingFilter(fields=[("pickup_time", "pickup_time")])
    distance_within = filters.NumberFilter(
        method="filter_by_distance_within",
        label="Filter data within a specific distance of the gps location, unit: km",
    )

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

    def filter_by_distance_within(self, qs, _, value):  # pragma: no cover
        gps_loc_in = self.data.get("gps_location")
        if gps_loc_in is None:
            return qs
        lat, lon = self.validate_gps_location(gps_loc_in.split(","))
        gps_location = Point(lat, lon, srid=4326)
        try:
            within_km = float(value)
        except ValueError:
            raise ValidationError("Invalid pickup_within value")
        degrees = self.kilometers_to_degrees(within_km)
        qs = qs.filter(pickup_pos__dwithin=(gps_location, degrees))
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

    def kilometers_to_degrees(self, km):  # pragma: no cover
        return km / 111.325
