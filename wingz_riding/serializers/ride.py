from wingz.restframework.serializers import BaseModelSerializer

from ..models import Ride


class RideModelSerializer(BaseModelSerializer):
    class Meta:
        model = Ride
        fields = "__all__"
