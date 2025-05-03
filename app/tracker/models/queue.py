from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

from . import TimeStampedMixin, UUIDMixin

User = get_user_model()


class Queue(UUIDMixin, TimeStampedMixin):
    key = models.CharField(
        max_length=50,
        unique=True,
        validators=[RegexValidator(regex="^[A-Z]+$", message="Только заглавные латинские буквы!", code="invalid_key")],
    )
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.key
