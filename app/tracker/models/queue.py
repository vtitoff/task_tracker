from django.contrib.auth import get_user_model
from django.db import models

from . import TimeStampedMixin, UUIDMixin

User = get_user_model()


class Queue(UUIDMixin, TimeStampedMixin):
    key = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
