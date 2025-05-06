from django.contrib.auth import get_user_model
from django.db import models
from .task import Task

from . import TimeStampedMixin, UUIDMixin

User = get_user_model()


class Comment(UUIDMixin, TimeStampedMixin):
    comment = models.TextField(max_length=5000)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-created"]
