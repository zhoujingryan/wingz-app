import random
from datetime import date

from django.contrib.gis.geos import Point
from django_fakery.faker_factory import factory

from wingz.utils.random import random_datetime, random_latitude, random_longitude
from wingz_riding.models import Ride
from wingz_sso.models import User


def run(*args):
    try:
        count, *_ = args
        count = int(count)
    except ValueError:
        count = 100

    users = User.objects.all()
    user_ids = [uid for uid in users.values_list("id_user", flat=True)]

    # create rides
    start_date = date(2023, 1, 1)
    end_date = date(2024, 10, 31)
    rides = []
    for i in range(count):
        pickup_lat = random_latitude()
        pickup_lon = random_longitude()
        r = factory.build(
            Ride,
            fields=dict(
                rider_id=random.choices(user_ids),
                driver_id=random.choices(user_ids),
                pickup_time=random_datetime(start_date, end_date),
                pickup_longitude=pickup_lon,
                pickup_latitude=pickup_lat,
                dropoff_longitude=random_longitude(),
                dropoff_latitude=random_latitude(),
            ),
        )
        r.pickup_pos = Point(pickup_lat, pickup_lon)
        rides.append(r)
    Ride.objects.bulk_create(rides, batch_size=1000)
