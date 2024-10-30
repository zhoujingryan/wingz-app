from wingz.restframework.serializers import BaseModelSerializer

from ..models import RideEvent


class RideEventModelSerializer(BaseModelSerializer):
    class Meta:
        model = RideEvent
        fields = "__all__"
