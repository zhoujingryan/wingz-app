from django.db import models

from wingz.db import BaseModel

from ..constants import RideStatus


class Ride(BaseModel):
    class Meta:
        db_table = "riding_ride"

    id_ride = models.BigAutoField(primary_key=True)
    status = models.CharField(
        max_length=32, choices=RideStatus.choices, help_text="ride status"
    )
    rider = models.ForeignKey(
        "wingz_sso.User",
        on_delete=models.DO_NOTHING,
        related_name="rider_rides",
        db_column="id_rider",
        null=True,
        db_constraint=False,
        db_index=True,
    )
    driver = models.ForeignKey(
        "wingz_sso.User",
        on_delete=models.DO_NOTHING,
        related_name="driver_rides",
        db_column="id_driver",
        null=True,
        db_constraint=False,
        db_index=True,
    )
    pickup_latitude = models.FloatField(help_text="latitude of pickup location")
    pickup_longitude = models.FloatField(help_text="longitude of pickup location")
    dropoff_latitude = models.FloatField(help_text="latitude of dropoff location")
    dropoff_longitude = models.FloatField(help_text="longitude of dropoff location")
    pickup_time = models.DateTimeField(help_text="pickup time")