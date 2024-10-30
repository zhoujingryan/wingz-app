from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "admin", "Admin"
    REGULAR = "regular_user", "Regular User"
