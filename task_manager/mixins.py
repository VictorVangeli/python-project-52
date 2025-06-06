from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class AuthRequiredMixin(LoginRequiredMixin):
    """
    Mixin to enforce user authentication.

    Displays an error message and redirects to the login page
    if the user is not authenticated.
    """

    auth_message = _("You are not logged in! Please log in.")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(reverse_lazy("login"))

        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(UserPassesTestMixin):
    """
    Mixin to restrict access based on object ownership.

    Prevents users from modifying objects that they do not own.
    Displays an error message and redirects if permission is denied.
    """

    permission_message = None
    permission_url = None

    def test_func(self):
        """
        Checks whether the current user is the owner of the object.
        """
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        """
        Handles the case where the user fails the ownership test.

        Shows an error message and redirects to the specified URL.
        """
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class DeleteProtectionMixin:
    """
    Mixin to protect against deletion of linked objects.

    Prevents deletion of an object if it is referenced by other related objects.
    Shows an error message and redirects if deletion is not allowed.
    """

    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)


class AuthorDeletionMixin(UserPassesTestMixin):
    """
    Mixin to restrict deletion to the item's author.

    Ensures that only the author of an object can delete it.
    Displays an error message and redirects if the current user is not the
        author.
    """

    author_message = None
    author_url = None

    def test_func(self):
        """
        Check if the current user is the author of the object.
        """
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        """
        Handle the case when the user is not the author.

        Displays an error message and redirects the user to a predefined URL.
        """
        messages.error(self.request, self.author_message)
        return redirect(self.author_url)
