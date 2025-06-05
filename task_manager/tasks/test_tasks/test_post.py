from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from task_manager.tasks.models import Task
from .testcase import TaskTestCase


class TestCreateTask(TaskTestCase):
    def test_create_valid_task(self) -> None:
        """
        Test that a valid task is successfully created via the task creation view.
        """
        task_data = self.test_task['create']['valid'].copy()
        response = self.client.post(
            reverse_lazy('task_create'),
            data=task_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))

        self.assertEqual(Task.objects.count(), self.count + 1)
        self.assertEqual(
            Task.objects.last().name,
            task_data['name']
        )
        self.assertEqual(
            Task.objects.last().author,
            self.user1
        )
        self.assertEqual(
            Task.objects.last().executor,
            self.user2
        )

    def test_create_fields_missing(self) -> None:
        """
        Test that the task creation form returns errors when required fields are missing.
        """
        task_data = self.test_task['create']['missing_fields'].copy()
        response = self.client.post(
            reverse_lazy('task_create'),
            data=task_data
        )
        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('name', errors)
        self.assertEqual(
            [error_help],
            errors['name']
        )

        self.assertIn('executor', errors)
        self.assertEqual(
            [error_help],
            errors['executor']
        )

        self.assertIn('status', errors)
        self.assertEqual(
            [error_help],
            errors['status']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), self.count)

    def test_create_task_exists(self) -> None:
        """
        Test that creating a task with a duplicate name returns a validation error.
        """
        task_data = self.test_task['create']['exists'].copy()
        response = self.client.post(
            reverse_lazy('task_create'),
            data=task_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Task with this Name already exists.')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), self.count)

    def test_create_long_field(self) -> None:
        """
        Test that creating a task with a name exceeding the maximum length
        returns a validation error.
        """
        task_data = self.test_task['create']['valid'].copy()
        task_data.update({'name': 'name' * 50})

        response = self.client.post(
            reverse_lazy('task_create'),
            data=task_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Ensure this value has at most 150 characters '
               f'(it has {len(task_data["name"])}).')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), self.count)


class TestUpdateTask(TaskTestCase):
    def test_update_task(self) -> None:
        """
        Test that a task can be successfully updated with valid data.
        """
        task_data = self.test_task['update'].copy()
        response = self.client.post(
            reverse_lazy('task_update', kwargs={'pk': 2}),
            data=task_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))

        self.assertEqual(Task.objects.count(), self.count)
        self.assertEqual(
            Task.objects.get(id=self.task2.id).name,
            task_data['name']
        )
        self.assertEqual(
            Task.objects.get(id=self.task2.id).executor.id,
            task_data['executor']
        )

    def test_update_task_not_logged_in(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when attempting to update a task.
        Also verifies that the task is not modified and the task count remains unchanged.
        """
        self.client.logout()

        task_data = self.test_task['update'].copy()
        response = self.client.post(
            reverse_lazy('task_update', kwargs={'pk': 2}),
            data=task_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(Task.objects.count(), self.count)
        self.assertNotEqual(
            Task.objects.get(id=self.task2.id).name,
            task_data['name']
        )


class TestDeleteTask(TaskTestCase):
    def test_delete_task(self) -> None:
        """
        Test that an authenticated user can successfully delete a task.
        Verifies redirection to the task list and confirms the task is removed from the database.
        """
        response = self.client.post(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertEqual(Task.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=self.task1.id)

    def test_delete_task_not_logged_in(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when attempting to delete a task.
        Also ensures that the task is not deleted from the database.
        """
        self.client.logout()

        response = self.client.post(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(Task.objects.count(), self.count)

    def test_delete_task_unauthorised(self) -> None:
        """
        Test that a logged-in user cannot delete a task they do not own.
        Verifies redirection to the task list and ensures the task remains in the database.
        """
        response = self.client.post(
            reverse_lazy('task_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertEqual(Task.objects.count(), self.count)
