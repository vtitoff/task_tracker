from django.urls import path
from .views import QueuesView, QueueDetailView, TaskDetailView, AddTask, AddQueue, ChangeTags


urlpatterns = [
    path("", QueuesView.as_view(), name="index"),
    path("queues/create_queue/", AddQueue.as_view(), name="create_queue"),
    path("queues/<slug:key>/", QueueDetailView.as_view(), name="queue"),
    path("queues/<slug:key>/create_task/", AddTask.as_view(), name="queue_create_task"),
    path("tasks/<slug:task_key>/change_tags/", ChangeTags.as_view(), name="change_tags"),
    path("tasks/<slug:task_key>/", TaskDetailView.as_view(), name="task"),
]
