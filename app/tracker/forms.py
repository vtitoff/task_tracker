from django import forms

from .models import Task, Queue, Tag, Comment


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"


class AddQueueForm(forms.ModelForm):
    class Meta:
        model = Queue
        fields = ["key", "name"]


class TaskStatusChangeForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["status"]
        widgets = {"status": forms.Select(attrs={"class": "form-control", "onchange": "this.form.submit()"})}


class TaskAssigneeChangeForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["assignee"]
        widgets = {"assignee": forms.Select(attrs={"class": "form-control", "onchange": "this.form.submit()"})}


class TaskDescriptionChangeForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["description"]
        widgets = {"description": forms.Textarea(attrs={"class": "form-control", "onchange": "this.form.submit()"})}


class TaskTagsChangeForm(forms.Form):
    tag = forms.CharField(max_length=255, label="Название тега")


class TaskCommentForm(forms.Form):
    comment = forms.CharField(max_length=5000, label="Текст комментария")
