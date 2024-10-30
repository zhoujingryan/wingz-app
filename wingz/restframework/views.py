from rest_framework import viewsets
from rest_framework.views import APIView


class BaseReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    pass


class BaseGenericViewSet(viewsets.GenericViewSet):
    pass


class BaseAPIView(APIView):
    pass
