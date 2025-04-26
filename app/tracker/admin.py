from .models import Queue, Tag, Status, Task

from django.contrib import admin


@admin.register(Queue)
class QueueAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "owner",
    )
    list_display_links = (
        "key",
        "owner",
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ("name",)
    list_display = ("name",)
    list_display_links = ("name",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    fields = ("name", "key")
    list_display = (
        "key",
        "name",
    )
    list_display_links = (
        "key",
        "name",
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "task_key",
        "author",
        "assignee",
        "status",
        "subject",
        "description",
    )
    list_display_links = (
        "task_key",
        "status",
        "author",
    )
