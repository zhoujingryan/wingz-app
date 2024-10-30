from rest_framework import pagination, viewsets
from rest_framework.views import APIView


class BasePageNumberPagination(pagination.PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


class BaseReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = BasePageNumberPagination


class BaseGenericViewSet(viewsets.GenericViewSet):
    pagination_class = BasePageNumberPagination


class BaseAPIView(APIView):
    pass
