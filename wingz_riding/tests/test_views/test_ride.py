import datetime

from django.urls import reverse
from django_fakery.faker_factory import factory

from wingz.restframework.tests import BaseAPITestCase
from wingz.utils.random import random_latitude, random_longitude
from wingz_riding.constants import RideStatus
from wingz_riding.models import Ride, RideEvent
from wingz_sso.constants import UserRole
from wingz_sso.models import User

ride_bp = factory.blueprint(Ride).fields(
    pickup_latitude=lambda i, f: random_latitude(),
    pickup_longitude=lambda i, f: random_longitude(),
)


class RideViewSetTestCase(BaseAPITestCase):

    def set_current_user(self):
        self.user = User.objects.create_user(
            email="regular@test.com", role=UserRole.REGULAR
        )

    def test_regular_user_cannot_view_ride_list(self):
        url = reverse("riding-rides-list")
        response = self.client.get(url)
        assert response.status_code == 403


class RideViewSetAdminTestCase(BaseAPITestCase):
    def test_admin_view_ride_list_success(self):
        url = reverse("riding-rides-list")
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.data
        assert "count" in data

    def test_filter_status_rides_list(self):
        ride_bp.m(quantity=3)(status=RideStatus.PICKUP)
        ride_bp.m(quantity=2)(status=RideStatus.EN_ROUTE)
        ride_bp.m(quantity=1)(status=RideStatus.DROPOFF)
        url = reverse("riding-rides-list") + f"?status={RideStatus.PICKUP}"
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.data
        assert data["count"] == 3

        url = reverse("riding-rides-list") + f"?status={RideStatus.EN_ROUTE}"
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.data
        assert data["count"] == 2

        url = reverse("riding-rides-list") + f"?status={RideStatus.DROPOFF}"
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.data
        assert data["count"] == 1

    def test_filter_rider_email_rides_list(self):
        u1 = factory.m(User)(email="test-rider1@email.com")
        u2 = factory.m(User)(email="test-rider2@email.com")
        u3 = factory.m(User)(email="example@email.com")

        ride_bp.m(quantity=3)(rider=u1)
        ride_bp.m(quantity=4)(rider=u2)
        ride_bp.m(quantity=5)(rider=u3)

        url = reverse("riding-rides-list") + "?rider__email__icontains=Email"
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.data
        assert data["count"] == 12

        url = reverse("riding-rides-list") + "?rider__email=example@email.com"
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.data
        assert data["count"] == 5

        url = reverse("riding-rides-list") + "?rider__email__icontains=rider"
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.data
        assert data["count"] == 7

    def test_rides_list_with_relational_data(self):
        rider = factory.m(User)(email="test-rider@email.com")
        driver = factory.m(User)(email="test-driver2@email.com")

        ride = ride_bp.m()(rider=rider, driver=driver)
        factory.m(RideEvent)(id_ride_event=1, ride=ride)
        factory.m(RideEvent)(id_ride_event=2, ride=ride)
        event = factory.m(RideEvent)(id_ride_event=3, ride=ride)
        event.created_at = datetime.datetime.now() - datetime.timedelta(hours=25)
        event.save()

        url = reverse("riding-rides-list")
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.data
        assert data["count"] == 1
        obj = data["results"][0]
        assert [e["id_ride_event"] for e in obj["todays_ride_events"]] == [2, 1]
        assert obj["rider"]["email"] == rider.email
        assert obj["driver"]["email"] == driver.email

    def test_rides_list_order_by_pickup_time(self):
        # invalid ordering field
        url = reverse("riding-rides-list") + "?ordering=abc"
        response = self.client.get(url)
        assert response.status_code == 400

        ride_bp.m(quantity=5)()
        url = reverse("riding-rides-list") + "?ordering=pickup_time"
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["count"] == 5

        data = response.data["results"]
        assert all(
            data[i]["pickup_time"] <= data[i + 1]["pickup_time"]
            for i in range(len(data) - 1)
        )

        url = reverse("riding-rides-list") + "?ordering=-pickup_time"
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.data["results"]
        assert all(
            data[i]["pickup_time"] >= data[i + 1]["pickup_time"]
            for i in range(len(data) - 1)
        )

    def test_rides_list_order_by_distance_failed(self):
        # gps_location is required
        url = reverse("riding-rides-list") + "?ordering=distance_to_pickup"
        response = self.client.get(url)
        assert response.status_code == 400

        # gps_location parameters error
        url = (
            reverse("riding-rides-list")
            + "?ordering=distance_to_pickup&gps_location=1,2,3"
        )
        response = self.client.get(url)
        assert response.status_code == 400

        # gps_location is not a valid number
        url = (
            reverse("riding-rides-list")
            + "?ordering=distance_to_pickup&gps_location=a,b"
        )
        response = self.client.get(url)
        assert response.status_code == 400

        # gps_location is not a valid coordinate
        url = (
            reverse("riding-rides-list")
            + "?ordering=distance_to_pickup&gps_location=100,20"
        )
        response = self.client.get(url)
        assert response.status_code == 400
        url = (
            reverse("riding-rides-list")
            + "?ordering=distance_to_pickup&gps_location=20,200"
        )
        response = self.client.get(url)
        assert response.status_code == 400

    def test_ride_list_sort_by_distance_to_pickup(self):
        bj_lat, bj_lon = (39.9, 116.4)
        sjz_lat, sjz_lon = (38.0, 114.5)
        xa_lat, xa_lon = (34.2, 108.9)
        beijing = ride_bp.m()(pickup_latitude=bj_lat, pickup_longitude=bj_lon)
        shijiazhuang = ride_bp.m()(pickup_latitude=sjz_lat, pickup_longitude=sjz_lon)
        xian = ride_bp.m()(pickup_latitude=xa_lat, pickup_longitude=xa_lon)
        url = (
            reverse("riding-rides-list")
            + f"?ordering=distance_to_pickup&gps_location={bj_lat},{bj_lon}"
        )
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.data["results"]
        assert [beijing.pk, shijiazhuang.pk, xian.pk] == [d["id_ride"] for d in data]

        cs_lat, cs_lon = (27.8, 113.2)
        url = (
            reverse("riding-rides-list")
            + f"?ordering=distance_to_pickup&gps_location={cs_lat},{cs_lon}"
        )
        response = self.client.get(url)
        assert response.status_code == 200
        data = response.data["results"]
        assert [xian.pk, shijiazhuang.pk, beijing.pk] == [d["id_ride"] for d in data]
