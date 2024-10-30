from wingz.restframework.serializers import BaseModelSerializer

from ..models import User


class UserModelSerializer(BaseModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]
