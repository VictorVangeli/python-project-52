from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView

from task_manager.mixins import AuthRequiredMixin, AuthorDeletionMixin
from .models import Task
from .forms import TaskForm
from .filters import TaskFilter


class TasksListView(AuthRequiredMixin, FilterView):
    template_name = "tasks/tasks.html"
    model = Task
    filterset_class = TaskFilter
    context_object_name = "tasks"

    def get_filterset(self, filterset_class):
        return filterset_class(
            self.request.GET, queryset=self.get_queryset(), request=self.request
        )

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "title": _("Tasks"),
            "button_text": _("Show"),
        }
        return context


class TaskDetailView(AuthRequiredMixin, DetailView):
    """
    Show one task details.

    Authorisation required.
    """

    template_name = "tasks/show_task.html"
    model = Task
    context_object_name = "task"

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "title": _("Task preview"),
        }
        return context


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new task.

    Authorisation required.
    """

    template_name = "form.html"
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks")
    success_message = _("Task successfully created")

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "title": _("Create task"),
            "button_text": _("Create"),
        }
        return context

    def form_valid(self, form):
        """
        Set current user as the task's author.
        """
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Edit existing task.

    Authorisation required.
    """

    template_name = "form.html"
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("tasks")
    success_message = _("Task successfully changed")

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "title": _("Task change"),
            "button_text": _("Change"),
        }
        return context


class TaskDeleteView(
    AuthRequiredMixin, AuthorDeletionMixin, SuccessMessageMixin, DeleteView
):
    """
    Delete existing task.

    Authorization required.
    Only the author can delete his tasks.
    """

    template_name = "tasks/delete_task.html"
    model = Task
    success_url = reverse_lazy("tasks")
    success_message = _("Task successfully deleted")
    author_message = _("The task can be deleted only by its author")
    author_url = reverse_lazy("tasks")

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "title": _("Delete task"),
            "button_text": _("Yes, delete"),
        }
        return context
