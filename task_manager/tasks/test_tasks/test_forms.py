from task_manager.tasks.forms import TaskForm
from .testcase import TaskTestCase


class TaskFormTest(TaskTestCase):
    def test_valid_form(self) -> None:
        """
        Test that the TaskForm is valid when provided with correct data.
        """
        task_data = self.test_task['create']['valid'].copy()
        form = TaskForm(data=task_data)

        self.assertTrue(form.is_valid())

    def test_invalid_form(self) -> None:
        """
        Test that the TaskForm is invalid when required fields are missing.
        """
        task_data = self.test_task['create']['missing_fields'].copy()
        form = TaskForm(data=task_data)

        self.assertFalse(form.is_valid())
