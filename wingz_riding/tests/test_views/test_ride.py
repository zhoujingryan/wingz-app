from django.urls import reverse
from django_fakery.faker_factory import factory

from wingz.restframework.tests import BaseAPITestCase
from wingz_riding.constants import RideStatus
from wingz_riding.models import Ride
from wingz_sso.constants import UserRole
from wingz_sso.models import User


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
        factory.m(Ride, quantity=3)(status=RideStatus.PICKUP)
        factory.m(Ride, quantity=2)(status=RideStatus.EN_ROUTE)
        factory.m(Ride, quantity=1)(status=RideStatus.DROPOFF)
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

        factory.m(Ride, quantity=3)(rider=u1)
        factory.m(Ride, quantity=4)(rider=u2)
        factory.m(Ride, quantity=5)(rider=u3)

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
