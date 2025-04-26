from django.contrib.auth import get_user_model
from django.db import models

from . import Queue, Status, Tag, TimeStampedMixin

User = get_user_model()


class Task(TimeStampedMixin):
    queue = models.ForeignKey(Queue, on_delete=models.CASCADE, related_name="tasks")
    number_in_queue = models.PositiveIntegerField(editable=False)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="authored_tasks", null=True)
    assignee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks")
    watchers = models.ManyToManyField(User, related_name="watching_tasks", blank=True)
    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)
    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("queue", "number_in_queue")
        ordering = ["-created"]

    @property
    def task_key(self):
        return f"{self.queue.key}-{self.number_in_queue}"

    def save(self, *args, **kwargs):
        if not self.pk:
            last_task = Task.objects.filter(queue=self.queue).order_by("-number_in_queue").first()
            self.number_in_queue = last_task.number_in_queue + 1 if last_task else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.task_key}: {self.subject}"
