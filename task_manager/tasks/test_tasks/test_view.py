from django.urls import reverse_lazy

from .testcase import TaskTestCase


class TestListTasks(TaskTestCase):
    def test_tasks_view(self) -> None:
        """
        Test that the task list view is accessible to an authenticated user.
        Verifies the response status and that the correct template is used.
        """
        response = self.client.get(reverse_lazy('tasks'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='tasks/tasks.html'
        )

    def test_tasks_content(self) -> None:
        """
        Test that the task list view returns the correct number of tasks for the user.
        Verifies the tasks in the context match the expected queryset.
        """
        response = self.client.get(reverse_lazy('tasks'))

        self.assertEqual(len(response.context['tasks']), self.count)
        self.assertQuerySetEqual(
            response.context['tasks'],
            self.tasks,
            ordered=False
        )

    def test_tasks_links(self) -> None:
        """
        Test that the task list page contains links to create, update, and delete tasks.
        Verifies the presence of these links for each task in the response content.
        """
        response = self.client.get(reverse_lazy('tasks'))

        self.assertContains(response, '/tasks/create/')

        for pk in range(1, self.count + 1):
            self.assertContains(response, f'/tasks/{pk}/update/')
            self.assertContains(response, f'/tasks/{pk}/delete/')

    def test_tasks_not_logged_in_view(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when attempting to access the task list view.
        """
        self.client.logout()

        response = self.client.get(reverse_lazy('tasks'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestFilterTasks(TaskTestCase):
    def test_filter_tasks_by_status(self) -> None:
        """
        Test that tasks can be filtered by status in the task list view.
        Verifies that only tasks with the specified status are included in the response.
        """
        response = self.client.get(
            reverse_lazy('tasks'),
            {'status': self.status1.pk}
        )

        self.assertEqual(response.context['tasks'].count(), 2)
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)

    def test_filter_tasks_by_executor(self) -> None:
        """
        Test that tasks can be filtered by executor in the task list view.
        Verifies that only tasks assigned to the specified executor are displayed.
        """
        response = self.client.get(
            reverse_lazy('tasks'),
            {'executor': self.user1.pk}
        )

        self.assertEqual(response.context['tasks'].count(), 1)
        self.assertNotContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)

    def test_filter_tasks_by_label(self) -> None:
        """
        Test that tasks can be filtered by label in the task list view.
        Verifies that only tasks with the specified label are displayed.
        """
        response = self.client.get(
            reverse_lazy('tasks'),
            {'labels': self.label2.pk}
        )

        self.assertEqual(response.context['tasks'].count(), 1)
        self.assertNotContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)

    def test_filter_tasks_by_own_tasks(self) -> None:
        """
        Test that the 'own tasks' filter returns only tasks created by the current user.
        Verifies that tasks created by others are excluded from the result.
        """
        response = self.client.get(
            reverse_lazy('tasks'),
            {'own_tasks': 'on'}
        )

        self.assertEqual(response.context['tasks'].count(), 2)
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)


class TestDetailedTask(TaskTestCase):
    def test_detailed_task_view(self) -> None:
        """
        Test that the detailed view of a task is accessible to an authenticated user.
        Verifies the response status and that the correct template is used.
        """
        response = self.client.get(
            reverse_lazy('task_show', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='tasks/show_task.html'
        )

    def test_detailed_task_content(self) -> None:
        """
        Test that the detailed task view displays all relevant task information.
        Verifies the presence of update/delete links, task fields, and associated labels in the response.
        """
        response = self.client.get(
            reverse_lazy('task_show', kwargs={'pk': 3})
        )

        labels = self.task3.labels.all()

        self.assertContains(response, '/tasks/3/update/')
        self.assertContains(response, '/tasks/3/delete/')

        self.assertContains(response, self.task3.name)
        self.assertContains(response, self.task3.description)
        self.assertContains(response, self.task3.author)
        self.assertContains(response, self.task3.executor)
        self.assertContains(response, self.task3.status)

        for label in labels:
            self.assertContains(response, label.name)

    def test_detailed_task_not_logged_in(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when attempting to view task details.
        """
        self.client.logout()

        response = self.client.get(
            reverse_lazy('task_show', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestCreateTaskView(TaskTestCase):
    def test_create_task_view(self) -> None:
        """
        Test that the task creation view is accessible to an authenticated user.
        Verifies the response status and that the correct template is used.
        """
        response = self.client.get(reverse_lazy('task_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_create_task_not_logged_in_view(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when attempting to access the task creation view.
        """
        self.client.logout()

        response = self.client.get(reverse_lazy('task_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestUpdateTaskView(TaskTestCase):
    def test_update_task_view(self) -> None:
        """
        Test that the task update view is accessible to the task author.
        Verifies the response status and that the correct template is used.
        """
        response = self.client.get(
            reverse_lazy('task_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_update_not_logged_in_view(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when attempting to access the task update view.
        """
        self.client.logout()

        response = self.client.get(
            reverse_lazy('task_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestDeleteTaskView(TaskTestCase):
    def test_delete_task_view(self) -> None:
        """
        Test that the task delete confirmation view is accessible to the task author.
        Verifies the response status and that the correct template is used.
        """
        response = self.client.get(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/delete_task.html')

    def test_delete_task_not_logged_in_view(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when attempting to access the task delete view.
        """
        self.client.logout()

        response = self.client.get(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete_task_unauthorised_view(self) -> None:
        """
        Test that a logged-in user cannot access the task delete view for a task they do not own.
        Verifies redirection to the task list page.
        """
        response = self.client.get(
            reverse_lazy('task_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))
