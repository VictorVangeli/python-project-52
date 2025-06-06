from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.utils import test_english, remove_rollbar
from task_manager.users.models import User


@test_english
@remove_rollbar
class HomeTestCase(TestCase):
    """
    Test case for the home page and authentication setup.

    This test case initializes a test client and creates a test user
    with predefined credentials for further testing.
    """

    def setUp(self) -> None:
        self.client = Client()

        self.credentials = {
            "username": "test_user",
            "password": "password_for_test_user",
        }
        self.user = User.objects.create_user(**self.credentials)


class HomePageTestCase(HomeTestCase):
    """
    Test case for the home page view and header links.

    This class extends the base HomeTestCase and includes tests for:
    - Successful loading of the index view
    - Presence of navigation links for authenticated users
    - Presence of appropriate links for unauthenticated users
    """

    def test_index_view(self) -> None:
        """
        Test that the index view loads correctly with a 200 status
        and uses the correct template.
        """
        response = self.client.get(reverse_lazy("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="index.html")
        self.assertContains(response, _("Task Manager"), status_code=200)

    def test_header_links_logged_in(self) -> None:
        """
        Test that authenticated users see links to statuses, labels, tasks, 
            and logout, and do not see the login link.
        """
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy("home"))

        self.assertContains(response, "/users/")
        self.assertContains(response, "/statuses/")
        self.assertContains(response, "/labels/")
        self.assertContains(response, "/tasks/")
        self.assertContains(response, "/logout/")

        self.assertNotContains(response, "/login/")

    def test_header_links_not_logged_in(self) -> None:
        """
        Test that unauthenticated users only see users and login links,
        and do not see links to statuses, labels, tasks, or logout.
        """
        response = self.client.get(reverse_lazy("home"))

        self.assertContains(response, "/users/")
        self.assertContains(response, "/login/")

        self.assertNotContains(response, "/statuses/")
        self.assertNotContains(response, "/labels/")
        self.assertNotContains(response, "/tasks/")
        self.assertNotContains(response, "/logout/")


class TestLoginUser(HomeTestCase):
    """
    Test case for the login functionality.

    This class tests the accessibility of the login view and the login process  
        itself, ensuring that a user can authenticate successfully and is 
        redirected to the homepage.
    """

    def test_user_login_view(self) -> None:
        """
        Test that the login view is accessible and uses the correct template.
        """
        response = self.client.get(reverse_lazy("login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="form.html")

    def test_user_login(self) -> None:
        """
        Test that a user can log in with valid credentials,
        is redirected to the home page, and becomes authenticated.
        """
        response = self.client.post(
            reverse_lazy("login"), self.credentials, follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy("home"))
        self.assertTrue(response.context["user"].is_authenticated)


class TestLogoutUser(HomeTestCase):
    """
    Test case for the logout functionality.

    Ensures that a logged-in user can successfully log out,
    is redirected to the homepage, and is no longer authenticated.
    """

    def test_user_logout(self) -> None:
        """
        Test the logout process.

        The test logs in a user, performs a logout via POST request,
        and verifies that the user is redirected and logged out.
        """
        self.client.force_login(self.user)

        response = self.client.post(reverse_lazy("logout"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy("home"))
        self.assertFalse(response.context["user"].is_authenticated)
