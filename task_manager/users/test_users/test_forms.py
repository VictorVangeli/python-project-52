from task_manager.users.forms import UserForm
from .testcase import UserTestCase


class UserFormTest(UserTestCase):
    def test_valid_form(self) -> None:
        """UserForm is valid with all required fields filled."""
        user_data = self.test_user['create']['valid'].copy()
        form = UserForm(data=user_data)

        self.assertTrue(form.is_valid())

    def test_invalid_form(self) -> None:
        """UserForm is invalid when required fields are missing."""
        user_data = self.test_user['create']['missing_fields'].copy()
        form = UserForm(data=user_data)

        self.assertFalse(form.is_valid())