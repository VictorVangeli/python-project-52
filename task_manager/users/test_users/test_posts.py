from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from task_manager.users.models import User
from .testcase import UserTestCase


class TestCreateUser(UserTestCase):
    def test_create_valid_user(self) -> None:
        """
        Test successful creation of a valid user.

        Verifies:
        - POST request to the sign-up page with valid data redirects to login.
        - New user is added to the database with correct username.
        """
        user_data = self.test_user["create"]["valid"].copy()
        response = self.client.post(reverse_lazy("sign_up"), data=user_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))

        self.assertEqual(User.objects.count(), self.count + 1)
        self.assertEqual(User.objects.last().username, user_data["username"])

    def test_create_fields_missing(self) -> None:
        """
        Test user creation with missing required fields.

        Verifies:
        - Form returns appropriate 'required field' errors for username, first_name, and last_name.
        - User is not created in the database.
        - Response status code is 200 (form re-rendered with errors).
        """
        user_data = self.test_user["create"]["missing_fields"].copy()
        response = self.client.post(reverse_lazy("sign_up"), data=user_data)
        errors = response.context["form"].errors
        error_help = _("This field is required.")

        self.assertIn("username", errors)
        self.assertEqual([error_help], errors["username"])

        self.assertIn("first_name", errors)
        self.assertEqual([error_help], errors["first_name"])

        self.assertIn("last_name", errors)
        self.assertEqual([error_help], errors["last_name"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_invalid_username(self) -> None:
        """
        Test user creation with an invalid username.

        Verifies:
        - The form returns an appropriate validation error for the 'username' field.
        - No new user is created in the database.
        - The response status code is 200 (form re-rendered with errors).
        """
        user_data = self.test_user["create"]["invalid"].copy()
        response = self.client.post(reverse_lazy("sign_up"), data=user_data)
        errors = response.context["form"].errors

        self.assertIn("username", errors)
        self.assertEqual(
            [
                _(
                    "Enter a valid username. This value may contain only "
                    "letters, numbers, and @/./+/-/_ characters."
                )
            ],
            errors["username"],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_username_exists(self) -> None:
        """
        Test user creation with an already existing username.

        Verifies:
        - The form raises a validation error indicating the username is taken.
        - No new user is created in the database.
        - The response returns a 200 status code with the form and errors.
        """
        user_data = self.test_user["create"]["exists"].copy()
        response = self.client.post(reverse_lazy("sign_up"), data=user_data)
        errors = response.context["form"].errors

        self.assertIn("username", errors)
        self.assertEqual(
            [_("A user with that username already exists.")], errors["username"]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_long_fields(self) -> None:
        """
        Test user creation with fields exceeding maximum length.

        Verifies:
        - Validation errors are raised for 'username', 'first_name', and 'last_name'
          when their lengths exceed 150 characters.
        - Appropriate error messages are shown for each field.
        - No user is created in the database.
        - Response status remains 200 with form errors.
        """
        user_data = self.test_user["create"]["valid"].copy()
        user_data.update({"username": "username" * 20})
        user_data.update({"first_name": "firstname" * 20})
        user_data.update({"last_name": "lastname" * 20})

        response = self.client.post(reverse_lazy("sign_up"), data=user_data)
        errors = response.context["form"].errors

        self.assertIn("username", errors)
        self.assertEqual(
            [
                _(
                    "Ensure this value has at most 150 characters "
                    f"(it has {len(user_data['username'])})."
                )
            ],
            errors["username"],
        )

        self.assertIn("first_name", errors)
        self.assertEqual(
            [
                _(
                    "Ensure this value has at most 150 characters "
                    f"(it has {len(user_data['first_name'])})."
                )
            ],
            errors["first_name"],
        )

        self.assertIn("last_name", errors)
        self.assertEqual(
            [
                _(
                    "Ensure this value has at most 150 characters "
                    f"(it has {len(user_data['last_name'])})."
                )
            ],
            errors["last_name"],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_missing(self) -> None:
        """
        Test user creation with missing passwords.

        Verifies:
        - Validation errors are raised for both 'password1' and 'password2' when omitted.
        - Correct error message is displayed for each missing password field.
        - No user is created in the database.
        - Response status is 200 with form errors rendered.
        """
        user_data = self.test_user["create"]["pass_missing"].copy()
        response = self.client.post(reverse_lazy("sign_up"), data=user_data)
        errors = response.context["form"].errors
        error_help = _("This field is required.")

        self.assertIn("password1", errors)
        self.assertEqual([error_help], errors["password1"])

        self.assertIn("password2", errors)
        self.assertEqual([error_help], errors["password2"])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_dont_match(self) -> None:
        """
        Test user creation with non-matching passwords.

        Verifies:
        - A validation error is raised for 'password2' when passwords do not match.
        - Correct error message is displayed.
        - No user is created in the database.
        - Response status is 200 with form errors shown.
        """
        user_data = self.test_user["create"]["pass_not_match"].copy()
        response = self.client.post(reverse_lazy("sign_up"), data=user_data)
        errors = response.context["form"].errors

        self.assertIn("password2", errors)
        self.assertEqual(
            [_("The two password fields didn’t match.")], errors["password2"]
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_too_short(self) -> None:
        """
        Test user creation with a too short password.

        Verifies:
        - Validation error is raised for 'password2' due to short password.
        - Correct error message is displayed about minimum length.
        - No new user is created in the database.
        - Response status is 200, indicating form was re-rendered with errors.
        """
        user_data = self.test_user["create"]["pass_too_short"].copy()
        response = self.client.post(reverse_lazy("sign_up"), data=user_data)
        errors = response.context["form"].errors

        self.assertIn("password2", errors)
        self.assertEqual(
            [
                _(
                    "This password is too short. "
                    "It must contain at least 8 characters."
                )
            ],
            errors["password2"],
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)


class TestUpdateUser(UserTestCase):
    def test_update_self(self) -> None:
        """
        Test that a user can successfully update their own profile.

        Verifies:
        - Authorized user (user2) can submit update form for their own data.
        - Redirects to the users list upon success.
        - No new user is created (user count remains the same).
        - User's updated data (e.g., first_name) is saved correctly.
        """
        self.client.force_login(self.user2)

        user_data = self.test_user["update"].copy()
        response = self.client.post(
            reverse_lazy("user_update", kwargs={"pk": 2}), data=user_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))

        self.assertEqual(User.objects.count(), self.count)
        self.assertEqual(
            User.objects.get(id=self.user2.id).first_name,
            user_data["first_name"],
        )

    def test_update_other(self) -> None:
        """
        Test that a user cannot update another user's profile.

        Verifies:
        - Authorized user (user1) attempts to update another user (user2).
        - Redirects to the users list due to lack of permissions.
        - No new user is created (user count remains the same).
        - Target user's data (e.g., first_name) remains unchanged.
        """
        self.client.force_login(self.user1)

        user_data = self.test_user["update"].copy()
        response = self.client.post(
            reverse_lazy("user_update", kwargs={"pk": 2}), data=user_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))

        self.assertEqual(User.objects.count(), self.count)
        self.assertNotEqual(
            User.objects.get(id=self.user2.id).first_name,
            user_data["first_name"],
        )


class TestDeleteUser(UserTestCase):
    def test_delete_self(self) -> None:
        """
        Test that a user can delete their own account.

        Verifies:
        - Authenticated user (user2) deletes their own account.
        - Redirect occurs to the users list.
        - User count is decreased by one.
        - Deleted user no longer exists in the database.
        """
        self.client.force_login(self.user4)

        response = self.client.post(
            reverse_lazy("user_delete", kwargs={"pk": 4})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))
        self.assertEqual(User.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=self.user4.id)

    def test_delete_other(self) -> None:
        """
        Test that a user cannot delete another user's account.

        Verifies:
        - Authenticated user (user1) attempts to delete user3.
        - Redirect occurs to the users list.
        - No change in the total number of users.
        """
        self.client.force_login(self.user1)

        response = self.client.post(
            reverse_lazy("user_delete", kwargs={"pk": 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))
        self.assertEqual(User.objects.count(), self.count)

    def test_delete_bound_user(self) -> None:
        """
        Test that a user bound to another object cannot be deleted.

        Verifies:
        - Authenticated user (user3) attempts to delete their account.
        - Deletion is blocked due to binding (e.g., foreign key constraint).
        - User is redirected to the users list.
        - Total number of users remains unchanged.
        """
        self.client.force_login(self.user3)

        response = self.client.post(
            reverse_lazy("user_delete", kwargs={"pk": 4})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("users"))
        self.assertEqual(User.objects.count(), self.count)
