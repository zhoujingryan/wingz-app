from .base import *  # noqa

DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.contrib.gis.db.backends.postgis",
        "NAME": "wingz-deploy",
        "USER": "postgres",
        "PASSWORD": "123456",
        "HOST": "192.168.124.8",
        "PORT": 9988,
    },
}
