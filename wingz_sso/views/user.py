from wingz.restframework.permissions import IsAdminUser
from wingz.restframework.views import BaseReadOnlyModelViewSet

from ..models import User
from ..serializers.user import UserModelSerializer


class UserViewSet(BaseReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (IsAdminUser,)
