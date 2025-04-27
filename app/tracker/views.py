from django.http import HttpResponse
from django.views.generic import TemplateView, DetailView
from .models import Queue


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
    # extra_context = {
    #     'title': '<UNK> <UNK>',
    # }
