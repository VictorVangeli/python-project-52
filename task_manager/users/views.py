# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import (
    AuthRequiredMixin,
    UserPermissionMixin,
    DeleteProtectionMixin,
)
from .models import User
from .forms import UserForm


class UsersListView(ListView):
    """
    Display a list of all registered users.

    This view renders a template that shows all users in the system.
    The context includes a localized title for display purposes.
    """

    template_name = "users/users.html"
    model = User
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Users")
        return context


class UserCreateView(SuccessMessageMixin, CreateView):
    """
    Register a new user.

    Displays a form for user registration. Upon successful submission, the user
    is redirected to the login page and a success message is shown.
    """

    template_name = "form.html"
    model = User
    form_class = UserForm
    success_url = reverse_lazy("login")
    success_message = _("User is successfully registered")

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "title": _("Create user"),
            "button_text": _("Register"),
        }
        return context


class UserUpdateView(
    AuthRequiredMixin, UserPermissionMixin, SuccessMessageMixin, UpdateView
):
    """
    Update the current user's information.

    Requires authentication. Users are only permitted to update their own
    information. Attempting to edit another user's data will result in an
    error message and redirection.
    """

    template_name = "form.html"
    model = User
    form_class = UserForm
    success_url = reverse_lazy("users")
    success_message = _("User is successfully updated")
    permission_message = _("You have no rights to change another user.")
    permission_url = reverse_lazy("users")

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "title": _("Update user"),
            "button_text": _("Update"),
        }
        return context


class UserDeleteView(
    AuthRequiredMixin,
    UserPermissionMixin,
    DeleteProtectionMixin,
    SuccessMessageMixin,
    DeleteView,
):
    """
    Delete the current user account.

    Requires authentication. A user can only delete their own account.
    Deletion is prohibited if the user is associated with other objects,
    such as tasks.
    """

    template_name = "users/delete_user.html"
    model = User
    success_url = reverse_lazy("users")
    success_message = _("User is successfully deleted")
    permission_message = _("You have no rights to change another user.")
    permission_url = reverse_lazy("users")
    protected_message = _("Unable to delete a user because he is being used")
    protected_url = reverse_lazy("users")

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "title": _("Delete user"),
            "button_text": _("Yes, delete"),
        }
        return context
