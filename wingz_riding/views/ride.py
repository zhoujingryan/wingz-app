import datetime

from django.db.models import Prefetch
from rest_framework import mixins

from wingz.restframework.permissions import IsAdminUser
from wingz.restframework.views import BaseGenericViewSet
from wingz_sso.serializers.user import UserModelSerializer

from ..filters.ride import RideFilter
from ..models import Ride, RideEvent
from ..serializers import RideEventModelSerializer, RideModelSerializer


class RideSerializer(RideModelSerializer):
    driver = UserModelSerializer()
    rider = UserModelSerializer()
    todays_ride_events = RideEventModelSerializer(many=True)


class RideViewSet(mixins.ListModelMixin, BaseGenericViewSet):
    """
    Rides
    """

    permission_classes = (IsAdminUser,)
    queryset = Ride.objects.order_by("-pk")
    serializer_class = RideSerializer
    filterset_class = RideFilter

    def get_queryset(self):
        now = datetime.datetime.now()
        _24_hours_ago = now - datetime.timedelta(hours=24)
        queryset = self.queryset.select_related("rider", "driver").prefetch_related(
            Prefetch(
                "events",
                queryset=RideEvent.objects.filter(
                    created_at__gte=_24_hours_ago
                ).order_by("-created_at"),
                to_attr="todays_ride_events",
            )
        )
        return queryset
