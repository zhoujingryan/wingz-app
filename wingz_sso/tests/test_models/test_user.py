from django.test import TestCase

from wingz_sso.models import User


class UserModelTest(TestCase):

    def test_user_create(self):
        email = "test@test.com"
        password = "123"
        User.objects.create_user(email=email, password=password)
        user = User.objects.filter(email=email).first()
        assert user is not None
        assert user.check_password(password)
        assert user.password != password

    def test_user_create_with_invalid_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="123")
