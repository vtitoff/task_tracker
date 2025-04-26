from django.db import models

from . import TimeStampedMixin


class Status(TimeStampedMixin):
    key = models.CharField(primary_key=True, max_length=50, unique=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.key

    class Meta:
        verbose_name_plural = "statuses"
