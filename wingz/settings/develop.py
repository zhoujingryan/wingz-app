from .base import *  # noqa

INSTALLED_APPS += [
    "debug_toolbar",
    "django.contrib.staticfiles",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["127.0.0.1", "localhost"]
