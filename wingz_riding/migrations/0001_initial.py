# Generated by Django 4.2.16 on 2024-11-01 03:03

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import wingz.db.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ride",
            fields=[
                (
                    "create_time",
                    models.DateTimeField(auto_now_add=True, db_column="create_time"),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now=True, db_column="update_time"),
                ),
                ("id_ride", models.BigAutoField(primary_key=True, serialize=False)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("en_route", "En Route"),
                            ("pickup", "Pickup"),
                            ("dropoff", "Drop Off"),
                        ],
                        help_text="ride status",
                        max_length=32,
                    ),
                ),
                (
                    "pickup_latitude",
                    models.FloatField(help_text="latitude of pickup location"),
                ),
                (
                    "pickup_longitude",
                    models.FloatField(help_text="longitude of pickup location"),
                ),
                (
                    "dropoff_latitude",
                    models.FloatField(help_text="latitude of dropoff location"),
                ),
                (
                    "dropoff_longitude",
                    models.FloatField(help_text="longitude of dropoff location"),
                ),
                ("pickup_time", models.DateTimeField(help_text="pickup time")),
                (
                    "pickup_pos",
                    django.contrib.gis.db.models.fields.PointField(srid=4326),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        db_column="id_driver",
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="driver_rides",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "rider",
                    models.ForeignKey(
                        db_column="id_rider",
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="rider_rides",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "riding_ride",
            },
            bases=(wingz.db.mixins.ModelDisplayMixin, models.Model),
        ),
        migrations.CreateModel(
            name="RideEvent",
            fields=[
                (
                    "create_time",
                    models.DateTimeField(auto_now_add=True, db_column="create_time"),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now=True, db_column="update_time"),
                ),
                (
                    "id_ride_event",
                    models.BigAutoField(primary_key=True, serialize=False),
                ),
                ("description", models.CharField(max_length=128)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                (
                    "ride",
                    models.ForeignKey(
                        db_column="id_ride",
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="events",
                        to="wingz_riding.ride",
                    ),
                ),
            ],
            options={
                "db_table": "riding_ride_event",
            },
            bases=(wingz.db.mixins.ModelDisplayMixin, models.Model),
        ),
    ]
