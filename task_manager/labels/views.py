from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin
from .models import Label
from .forms import LabelForm


class LabelsListView(AuthRequiredMixin, ListView):
    """
    Show all labels.

    Authorisation required.
    """

    template_name = "labels/labels.html"
    model = Label
    context_object_name = "labels"

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "title": _("Labels"),
        }
        return context


class LabelCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new label.

    Authorisation required.
    """

    template_name = "form.html"
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy("labels")
    success_message = _("Label successfully created")

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "title": _("Create label"),
            "button_text": _("Create"),
        }
        return context


class LabelUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Edit existing label.

    Authorisation required.
    """

    template_name = "form.html"
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy("labels")
    success_message = _("Label successfully changed")

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "title": _("Change label"),
            "button_text": _("Change"),
        }
        return context


class LabelDeleteView(
    AuthRequiredMixin, DeleteProtectionMixin, SuccessMessageMixin, DeleteView
):
    """
    Delete existing label.

    Authorization required.
    If the label is associated with at least one task it cannot be deleted.
    """

    template_name = "labels/delete_label.html"
    model = Label
    success_url = reverse_lazy("labels")
    success_message = _("Label successfully deleted")
    protected_message = _(
        "It is not possible to delete a label because it is in use"
    )
    protected_url = reverse_lazy("labels")

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "title": _("Delete label"),
            "button_text": _("Yes, delete"),
        }
        return context
