from django import forms

from .models import Task, Queue


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"


class AddQueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = "__all__"
