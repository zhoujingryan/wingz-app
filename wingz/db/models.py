from django.db import models

from .mixins import ModelDisplayMixin


class BaseModel(ModelDisplayMixin, models.Model):
    class Meta:
        abstract = True

    create_time = models.DateTimeField(db_column="create_time", auto_now_add=True)
    update_time = models.DateTimeField(db_column="update_time", auto_now=True)
