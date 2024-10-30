from django.conf import settings
from django.forms import model_to_dict


class ModelDisplayMixin:
    DISPLAY_FIELDS = None

    def __repr__(self):
        if settings.DEBUG:
            displays = model_to_dict(self, fields=self.DISPLAY_FIELDS)
            return "<{}: \n{}>".format(
                self.__class__.__name__,
                "\t\n".join([f"{k}={v}" for k, v in displays.items()]),
            )
        return super().__repr__()
