from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView
from .models import Queue, Task
from .forms import AddTaskForm, AddQueueForm, TaskStatusChangeForm
from django.contrib import messages


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


class TaskDetailView(DetailView):
    template_name = "task_detail.html"
    model = Task

    def get_object(self):
        task_key = self.kwargs.get("task_key")
        try:
            queue_key, task_number = task_key.split("-")
        except ValueError:
            raise Http404("Invalid task key format")

        return get_object_or_404(
            Task.objects.select_related("queue"), queue__key=queue_key, number_in_queue=task_number
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["status_form"] = TaskStatusChangeForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        form = TaskStatusChangeForm(request.POST, instance=task)

        if form.is_valid():
            if request.user == task.author or request.user == task.assignee:
                form.save()
                messages.success(request, "Статус обновлен!")
            else:
                messages.error(request, "Нет прав для изменения статуса")
        return self.get(request, *args, **kwargs)


class AddTask(CreateView):
    form_class = AddTaskForm
    template_name = "add_task.html"
    success_url = reverse_lazy("index")


class AddQueue(CreateView):
    form_class = AddQueueForm
    template_name = "add_queue.html"
    success_url = reverse_lazy("index")
