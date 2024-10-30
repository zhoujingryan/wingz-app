from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class PasswordLoginAPIView(TokenObtainPairView):
    permission_classes = ()
    serializer_class = TokenObtainSerializer

    @swagger_auto_schema(
        responses={200: TokenObtainSerializer()},
        operation_summary="user password login",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)  # pragma: no cover
