from django.urls import path
from .views import QueuesView, QueueDetailView, TaskDetailView


urlpatterns = [
    path("", QueuesView.as_view(), name="test"),
    path("queues/<slug:key>/", QueueDetailView.as_view(), name="queue"),
    path("tasks/<slug:task_key>/", TaskDetailView.as_view(), name="task"),
]
