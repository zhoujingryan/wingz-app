from django.db import models


class RideStatus(models.TextChoices):
    EN_ROUTE = "en_route", "En Route"
    PICKUP = "pickup", "Pickup"
    DROPOFF = "dropoff", "Drop Off"
