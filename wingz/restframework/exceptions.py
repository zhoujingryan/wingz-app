from django.http import Http404
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import exception_handler


class BaseError(Exception):
    code = 1
    message = "API Error"

    def __init__(self, message=None):
        if message is not None:
            self.message = message

    def __str__(self):
        return self.message

    def get_response_data(self):
        return {"errors": [{"code": self.code, "message": self.message}]}

    def __repr__(self):
        return "<%s>" % self.__class__.__name__


def error_handler(exc, context):
    if isinstance(exc, BaseError):
        response = Response(exc.get_response_data(), status=402)
    else:
        if isinstance(exc, Http404):
            exc = exceptions.NotFound(detail=str(exc) or None)
        response = exception_handler(exc, context)
    return response
