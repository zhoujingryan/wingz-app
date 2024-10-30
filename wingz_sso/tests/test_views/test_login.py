from django.urls import reverse

from wingz.restframework.tests import BaseAPITestCase
from wingz_sso.models import User


class UserPasswordLoginTestCase(BaseAPITestCase):

    def set_current_user(self):
        pass

    def test_login_success(self):
        url = reverse("sso-password-login")
        email = "test@test.com"
        password = "123456"
        User.objects.create_user(email=email, password=password)

        data = {"email": email, "password": password}
        response = self.client.post(url, data, format="json")
        assert response.status_code == 200
        assert "access" in response.data
