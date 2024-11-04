from .base import *  # noqa

INSTALLED_APPS += [
    "debug_toolbar",
    "django.contrib.staticfiles",
]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

INTERNAL_IPS = ["127.0.0.1", "localhost"]

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "wingz",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "127.0.0.1",
        "PORT": 5432,
    },
}
