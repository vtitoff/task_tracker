from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, CreateView, View
from .models import Queue, Task, Tag, Comment
from .forms import (
    AddTaskForm,
    AddQueueForm,
    TaskStatusChangeForm,
    TaskAssigneeChangeForm,
    TaskDescriptionChangeForm,
    TaskTagsChangeForm,
    TaskCommentForm,
)
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
        context["assignee_form"] = TaskAssigneeChangeForm(instance=self.object)
        context["description_form"] = TaskDescriptionChangeForm(instance=self.object)
        context["tags_form"] = TaskTagsChangeForm()
        context["comments_form"] = TaskCommentForm()
        return context

    def handle_task_forms(self, request, task):
        form_type = request.POST.get("form_type")

        if not form_type:
            messages.error(request, "Не указан тип формы")
            return

        handlers = {
            "status": self.handle_status_form,
            "assignee": self.handle_assignee_form,
            "description": self.handle_description_form,
            "tags": self.handle_tags_form,
            "comment": self.handle_comment_form,
        }

        handler = handlers.get(form_type)

        return handler(request, task)

    def handle_status_form(self, request, task):
        form = TaskStatusChangeForm(request.POST, instance=task)

        if form.is_valid():
            form.save()

    def handle_assignee_form(self, request, task):
        form = TaskAssigneeChangeForm(request.POST, instance=task)
        if form.is_valid():
            form.save()

    def handle_description_form(self, request, task):
        form = TaskDescriptionChangeForm(request.POST, instance=task)
        if form.is_valid():
            form.save()

    def handle_tags_form(self, request, task):
        form = TaskTagsChangeForm(request.POST)
        task_key = self.kwargs.get("task_key")
        if form.is_valid():
            tag = Tag.objects.get_or_create(name=form.cleaned_data["tag"])
            queue_key, task_number = task_key.split("-")
            task = get_object_or_404(
                Task.objects.select_related("queue"), queue__key=queue_key, number_in_queue=task_number
            )
            if tag[0] in task.tags.all():
                task.tags.remove(tag[0])
            else:
                task.tags.add(tag[0])

        return redirect("task", task_key=task_key, permanent=True)

    def handle_comment_form(self, request, task):
        form = TaskCommentForm(request.POST)
        task_key = self.kwargs.get("task_key")
        if form.is_valid():
            queue_key, task_number = task_key.split("-")
            task = get_object_or_404(
                Task.objects.select_related("queue"), queue__key=queue_key, number_in_queue=task_number
            )
            Comment.objects.create(comment=form.cleaned_data["comment"], task=task, owner=request.user)
        return redirect("task", task_key=task_key, permanent=True)

    def post(self, request, *args, **kwargs):
        task = self.get_object()
        response = self.handle_task_forms(request, task)
        return response or self.get(request, *args, **kwargs)


class AddTask(CreateView):
    form_class = AddTaskForm
    template_name = "add_task.html"
    success_url = reverse_lazy("index")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["queue_key"] = self.kwargs.get("key")
        return context


class AddQueue(CreateView):
    form_class = AddQueueForm
    template_name = "add_queue.html"
    success_url = reverse_lazy("index")


class Login(LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"


class Logout(LogoutView):
    template_name = "logout.html"
