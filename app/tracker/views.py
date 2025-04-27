from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView
from .models import Queue, Task


class QueuesView(TemplateView):
    template_name = "index.html"
    extra_context = {
        "title": "Главная страница",
        "queues": Queue.objects.all(),
        "cat_selected": 0,
    }


class QueueDetailView(DetailView):
    template_name = "queue_detail.html"
    model = Queue
    slug_field = "key"
    slug_url_kwarg = "key"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_queue = self.object
        context["tasks"] = Task.objects.filter(queue=current_queue).order_by("number_in_queue")
        return context
