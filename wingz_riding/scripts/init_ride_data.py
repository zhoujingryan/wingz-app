import random
from datetime import date

from django.contrib.gis.geos import Point
from django_fakery.faker_factory import factory

from wingz_riding.models import Ride
from wingz_sso.models import User


def run(*args):
    try:
        count, *_ = args
        count = int(count)
    except ValueError:
        count = 100

    users = list(User.objects.all())

    # create rides
    start_date = date(2023, 1, 1)
    end_date = date(2024, 10, 31)
    fake = factory.fake
    ride_bp = factory.blueprint(Ride).fields(
        pickup_time=lambda i, _: fake.date_time_between(start_date, end_date),
        dropoff_latitude=lambda i, _: fake.latitude(),
        dropoff_longitude=lambda i, _: fake.longitude(),
    )
    rides = []
    for i in range(count):
        pickup_lat = fake.latitude()
        pickup_lon = fake.longitude()
        r = ride_bp.b()(
            rider=random.choice(users),
            driver=random.choice(users),
            pickup_longitude=pickup_lon,
            pickup_latitude=pickup_lat,
            pickup_pos=Point(float(pickup_lat), float(pickup_lon)),
        )
        rides.append(r)
    Ride.objects.bulk_create(rides, batch_size=1000)
