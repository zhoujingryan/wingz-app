from django.urls import include, path
from rest_framework.routers import SimpleRouter

from wingz_riding.views.ride import RideViewSet

router = SimpleRouter()
router.register("rides", RideViewSet, basename="riding-rides")

urlpatterns = [
    path("", include(router.urls)),
]
