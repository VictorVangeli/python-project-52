from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from django.views.generic import TemplateView


class IndexView(TemplateView):
    """
    Display the homepage of the task manager.

    This view renders the main index page and sets the page title in the context.
    """

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Task manager")
        return context


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Handle user login.

    Renders the login form, authenticates the user, and redirects to the home page upon success.
    Adds title and button text to the template context.
    """

    template_name = "form.html"
    next_page = reverse_lazy("home")
    success_message = _("You are logged in")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = _("Login")
        context["button_text"] = _("Enter")
        return context


class UserLogoutView(LogoutView):
    """
    Handle user logout.

    Logs the user out and redirects to the home page.
    Displays an informational message upon logout.
    """

    next_page = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)


def test_rollbar_view(request):
    """
    Test Rollbar integration by triggering an intentional error.

    This view is used to verify that Rollbar correctly captures and reports
    uncaught exceptions. It deliberately raises an AttributeError by
    attempting to call a method on `None`.
    """
    a = None
    a.test()
