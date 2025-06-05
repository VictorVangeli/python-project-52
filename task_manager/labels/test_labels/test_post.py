from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from task_manager.labels.models import Label
from .testcase import LabelTestCase


class TestCreateLabel(LabelTestCase):
    def test_create_valid_label(self) -> None:
        """
        Test that a new label is successfully created via the create view with valid data.
        Verifies redirection, label count increment, and correctness of the created label.
        """
        label_data = self.test_label['create']['valid'].copy()
        response = self.client.post(
            reverse_lazy('label_create'),
            data=label_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels'))

        self.assertEqual(Label.objects.count(), self.count + 1)
        self.assertEqual(
            Label.objects.last().name,
            label_data['name']
        )

    def test_create_fields_missing(self) -> None:
        """
        Test that label creation fails when required fields are missing.
        Verifies that form errors are returned and no new label is added to the database.
        """
        label_data = self.test_label['create']['missing_fields'].copy()
        response = self.client.post(
            reverse_lazy('label_create'),
            data=label_data
        )
        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('name', errors)
        self.assertEqual(
            [error_help],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), self.count)

    def test_create_label_exists(self) -> None:
        """
        Test that label creation fails when a label with the same name already exists.
        Verifies that a validation error is shown and no duplicate label is created.
        """
        label_data = self.test_label['create']['exists'].copy()
        response = self.client.post(
            reverse_lazy('label_create'),
            data=label_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Label with this Name already exists.')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), self.count)

    def test_create_long_field(self) -> None:
        """
        Test that label creation fails when the 'name' field exceeds the maximum allowed length.
        Verifies that a validation error is returned and no new label is created.
        """
        label_data = self.test_label['create']['valid'].copy()
        label_data.update({'name': 'name' * 50})

        response = self.client.post(
            reverse_lazy('label_create'),
            data=label_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Ensure this value has at most 150 characters '
               f'(it has {len(label_data["name"])}).')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), self.count)


class TestUpdateLabel(LabelTestCase):
    def test_update_label(self) -> None:
        """
        Test that an existing label can be successfully updated with valid data.
        Verifies redirection, unchanged label count, and updated field value.
        """
        label_data = self.test_label['update'].copy()
        response = self.client.post(
            reverse_lazy('label_update', kwargs={'pk': 2}),
            data=label_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels'))

        self.assertEqual(Label.objects.count(), self.count)
        self.assertEqual(
            Label.objects.get(id=self.label2.id).name,
            label_data['name']
        )

    def test_update_label_not_logged_in(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when attempting to update a label.
        Verifies that the label remains unchanged.
        """
        self.client.logout()

        label_data = self.test_label['update'].copy()
        response = self.client.post(
            reverse_lazy('label_update', kwargs={'pk': 2}),
            data=label_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(Label.objects.count(), self.count)
        self.assertNotEqual(
            Label.objects.get(id=self.label2.id).name,
            label_data['name']
        )


class TestDeleteLabel(LabelTestCase):
    def test_delete_label(self) -> None:
        """
        Test that an authenticated user can successfully delete a label.
        Verifies redirection and confirms the label is removed from the database.
        """
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels'))
        self.assertEqual(Label.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=self.label3.id)

    def test_delete_label_not_logged_in(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when attempting to delete a label.
        Verifies that the label is not removed from the database.
        """
        self.client.logout()

        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(Label.objects.count(), self.count)

    def test_delete_bound_label(self) -> None:
        """
        Test that a label bound to existing tasks cannot be deleted.
        Verifies redirection and that the label count remains unchanged.
        """
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels'))
        self.assertEqual(Label.objects.count(), self.count)