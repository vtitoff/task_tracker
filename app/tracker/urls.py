from django.urls import path
from .views import QueuesView, QueueDetailView


urlpatterns = [
    path("", QueuesView.as_view(), name="test"),
    path("queue/<slug:key>/", QueueDetailView.as_view(), name="queue"),
]
