from django.conf import settings


class ModelDisplayMixin:
    DISPLAY_FIELDS = None

    def __repr__(self):
        if settings.DEBUG:
            return "<{}: \n{}>".format(
                self.__class__.__name__,
                "\t\n".join([f"{k}={v}" for k, v in self.__dict__.items()]),
            )
        model_fields = [f.name for f in self._meta.fields]
        displays = self.DISPLAY_FIELDS if self.DISPLAY_FIELDS else model_fields
        for name in displays:
            if name not in self.__dict__:
                continue
            return "<{} object {}: {}>".format(
                self.__class__.__name__,
                name,
                self.__dict__[name],
            )
        return super(ModelDisplayMixin, self).__repr__()
