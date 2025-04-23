from django.core.validators import RegexValidator
from django.db import models

from . import TimeStampedMixin


class Tag(TimeStampedMixin):
    name = models.CharField(
        primary_key=True, editable=False, max_length=50, unique=True, validators=[RegexValidator(regex="^[a-z0-9_]+$")]
    )

    def __str__(self):
        return self.name
