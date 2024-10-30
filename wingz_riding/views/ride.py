from rest_framework import mixins

from wingz.restframework.permissions import IsAdminUser
from wingz.restframework.views import BaseGenericViewSet

from ..filters.ride import RideFilter
from ..models import Ride
from ..serializers.ride import RideModelSerializer


class RideViewSet(mixins.ListModelMixin, BaseGenericViewSet):
    permission_classes = (IsAdminUser,)
    queryset = Ride.objects.order_by("-pk")
    serializer_class = RideModelSerializer
    filterset_class = RideFilter
