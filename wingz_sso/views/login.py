from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class PasswordLoginResponseSerializer(serializers.Serializer):
    access = serializers.CharField(label="access token")
    refresh = serializers.CharField(label="refresh token")


class PasswordLoginAPIView(TokenObtainPairView):
    permission_classes = ()
    serializer_class = TokenObtainPairSerializer

    @swagger_auto_schema(
        responses={200: PasswordLoginResponseSerializer()},
        operation_summary="user password login",
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
