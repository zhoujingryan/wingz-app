from django.urls import reverse

from wingz.restframework.tests import BaseAPITestCase
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
