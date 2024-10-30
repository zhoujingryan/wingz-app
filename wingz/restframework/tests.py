from rest_framework.test import APITestCase
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from wingz_sso.models import User


class BaseAPITestCase(APITestCase):
    def __init__(self, methodName="runTest"):
        super(BaseAPITestCase, self).__init__(methodName)
        self.user = None

    @classmethod
    def setUpClass(cls):
        super(BaseAPITestCase, cls).setUpClass()

    def set_current_user(self):
        self.user, _ = User.objects.get_or_create(
            email="test@test.com", role=User.UserRole.ADMIN
        )

    def setUp(self):
        self.set_current_user()
        if self.user:
            refresh = RefreshToken.for_user(self.user)
            self.access_token = refresh.access_token
            self.client.credentials(
                HTTP_AUTHORIZATION=f"{api_settings.AUTH_HEADER_TYPES[0]} {str(self.access_token)}"
            )
