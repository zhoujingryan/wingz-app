import datetime
import random
from datetime import date

from django_fakery.faker_factory import factory

from wingz_riding.models import Ride, RideEvent


def run(*args):
    try:
        count, *_ = args
        count = int(count)
    except ValueError:
        count = 100

    rides = list(Ride.objects.filter(pickup_time__gt=date(2024, 1, 1)))
    fake = factory.fake

    pickup_desc = "Status changed to pickup"
    dropoff_desc = "Status changed to dropoff"
    events = []
    for i in range(count):
        ride = random.choice(rides)
        # create pickup event
        events.append(
            RideEvent(
                ride=ride,
                description=pickup_desc,
                created_at=ride.pickup_time,
            )
        )
        # create dropoff event
        if fake.boolean():
            dropoff_time = fake.date_time_between(
                ride.pickup_time, ride.pickup_time + datetime.timedelta(hours=3)
            )
            events.append(
                RideEvent(
                    ride=ride,
                    description=dropoff_desc,
                    created_at=dropoff_time,
                )
            )
    RideEvent.objects.bulk_create(events, batch_size=1000)
