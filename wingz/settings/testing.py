from .base import *  # noqa

TESTING = True

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.mysql",
        "NAME": ":memory:",
    }
}
