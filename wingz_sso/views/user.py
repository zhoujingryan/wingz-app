from wingz.restframework.permissions import IsAdminUser
from wingz.restframework.views import BaseReadOnlyModelViewSet

from ..models import User
from ..serializers.user import UserModelSerializer


class UserViewSet(BaseReadOnlyModelViewSet):
    """Users Admin"""

    queryset = User.objects.order_by("-id_user")
    serializer_class = UserModelSerializer
    permission_classes = (IsAdminUser,)
