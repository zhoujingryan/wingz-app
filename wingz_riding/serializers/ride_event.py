from wingz.restframework.serializers import BaseModelSerializer

from ..models import RideEvent


class RideEventModelSerializer(BaseModelSerializer):
    class Meta:
        model = RideEvent
        exclude = ("create_time", "update_time")
