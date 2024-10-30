from django.urls import include, path
from rest_framework.routers import SimpleRouter

from wingz_sso.views.login import PasswordLoginAPIView
from wingz_sso.views.user import UserViewSet

router = SimpleRouter()
router.register(r"users", UserViewSet, basename="users")


urlpatterns = [
    path("", include(router.urls)),
    path(
        r"login/",
        PasswordLoginAPIView.as_view(),
        name="sso-password-login",
    ),
]
