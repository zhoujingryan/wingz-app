from django.db import models

from wingz.db import BaseModel


class RideEvent(BaseModel):
    class Meta:
        db_table = "riding_ride_event"

    id_ride_event = models.BigAutoField(primary_key=True)
    ride = models.ForeignKey(
        "Ride",
        on_delete=models.DO_NOTHING,
        related_name="events",
        db_column="id_ride",
        db_constraint=False,
        null=True,
        db_index=True,
    )
    description = models.CharField(max_length=128)
    created_at = models.DateTimeField(db_index=True)
