from django.urls import reverse_lazy

from .testcase import UserTestCase


class TestListUsers(UserTestCase):
    def test_users_view(self) -> None:
        """
        Test that the users list view returns a successful response.

        Verifies:
        - The view returns HTTP 200 status.
        - The correct template ('users/users.html') is used.
        """
        response = self.client.get(reverse_lazy("users"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="users/users.html")

    def test_users_content(self) -> None:
        """
        Test that the users list view contains all expected users.

        Verifies:
        - The number of users in the context matches the expected count.
        - The queryset of users in the context matches the test dataset.
        """
        response = self.client.get(reverse_lazy("users"))

        self.assertEqual(len(response.context["users"]), self.count)
        self.assertQuerySetEqual(
            response.context["users"], self.users, ordered=False
        )

    def test_users_links(self) -> None:
        """
        Test that the users list page contains correct links.

        Verifies:
        - The link to create a new user is present.
        - Each user has links for update and delete actions.
        """
        response = self.client.get(reverse_lazy("users"))

        self.assertContains(response, "/users/create/")

        for pk in range(1, self.count + 1):
            self.assertContains(response, f"/users/{pk}/update/")
            self.assertContains(response, f"/users/{pk}/delete/")


class TestCreateUserView(UserTestCase):
    def test_sign_up_view(self) -> None:
        """
        Test that the sign-up view returns the correct response.

        Verifies:
        - The sign-up page is accessible (status code 200).
        - The correct template 'form.html' is used.
        """
        response = self.client.get(reverse_lazy("sign_up"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="form.html")


class TestUpdateUserView(UserTestCase):
    def test_update_self_view(self) -> None:
        """
        Test that a user can access their own update view.

        Verifies:
        - The page loads successfully (status code 200).
        - The correct template 'form.html' is used.
        """
        self.client.force_login(self.user2)

        response = self.client.get(
            reverse_lazy("user_update", kwargs={"pk": 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="form.html")

    def test_update_not_logged_in_view(self) -> None:
        """
        Test that an unauthenticated user is redirected when trying to access the update view.

        Verifies:
        - Response status is 302 (redirect).
        - Redirects to the login page.
        """
        response = self.client.get(
            reverse_lazy("user_update", kwargs={"pk": 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))

    def test_update_other_view(self) -> None:
        """
        Test that a logged-in user cannot access the update view of another user.

        Verifies:
        - Response status is 302 (redirect).
        - Redirects to the users list page instead of allowing access.
        """
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse_lazy("user_update", kwargs={"pk": 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))


class TestDeleteUserView(UserTestCase):
    def test_delete_self_view(self) -> None:
        """
        Test that a logged-in user can access their own delete confirmation view.

        Verifies:
        - Response status is 200 (OK).
        - Correct delete confirmation template is used.
        """
        self.client.force_login(self.user3)

        response = self.client.get(
            reverse_lazy("user_delete", kwargs={"pk": 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name="users/delete_user.html"
        )

    def test_delete_not_logged_in_view(self) -> None:
        """
        Test that an unauthenticated user is redirected when accessing the delete view.

        Verifies:
        - Response status is 302 (redirect).
        - User is redirected to the login page.
        """
        response = self.client.get(
            reverse_lazy("user_delete", kwargs={"pk": 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))

    def test_delete_other_view(self) -> None:
        """
        Test that a user cannot access the delete view for another user's profile.

        Verifies:
        - Logged-in user1 is not allowed to view delete page for user3.
        - Response status is 302 (redirect).
        - User is redirected to the users list page.
        """
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse_lazy("user_delete", kwargs={"pk": 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))
