from django.urls import reverse_lazy

from .testcase import LabelTestCase


class TestListLabels(LabelTestCase):
    def test_labels_view(self) -> None:
        """
        Test that the label list view is accessible to an authenticated user.
        Verifies the response status and that the correct template is used.
        """
        response = self.client.get(reverse_lazy("labels"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="labels/labels.html")

    def test_labels_content(self) -> None:
        """
        Test that the label list view returns the correct number of labels.
        Verifies that the labels in the context match the expected queryset.
        """
        response = self.client.get(reverse_lazy("labels"))

        self.assertEqual(len(response.context["labels"]), self.count)
        self.assertQuerySetEqual(
            response.context["labels"], self.labels, ordered=False
        )

    def test_labels_links(self) -> None:
        """
        Test that the label list page contains links to create, update, and
            delete labels.
        Verifies the presence of these links for each label in the response 
            content.
        """
        response = self.client.get(reverse_lazy("labels"))

        self.assertContains(response, "/labels/create/")

        for pk in range(1, self.count + 1):
            self.assertContains(response, f"/labels/{pk}/update/")
            self.assertContains(response, f"/labels/{pk}/delete/")

    def test_labels_not_logged_in_view(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when
            attempting to access the label list view.
        """
        self.client.logout()

        response = self.client.get(reverse_lazy("labels"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))


class TestCreateLabelView(LabelTestCase):
    def test_create_label_view(self) -> None:
        """
        Test that the label creation view is accessible to an authenticated 
            user.
        Verifies the response status and that the correct template is used.
        """
        response = self.client.get(reverse_lazy("label_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="form.html")

    def test_create_label_not_logged_in_view(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when
            attempting to access the label creation view.
        """
        self.client.logout()

        response = self.client.get(reverse_lazy("label_create"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))


class TestUpdateLabelView(LabelTestCase):
    def test_update_label_view(self) -> None:
        """
        Test that the label update view is accessible to an authenticated user.
        Verifies the response status and that the correct template is used.
        """
        response = self.client.get(
            reverse_lazy("label_update", kwargs={"pk": 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name="form.html")

    def test_update_not_logged_in_view(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when
            attempting to access the label update view.
        """
        self.client.logout()

        response = self.client.get(
            reverse_lazy("label_update", kwargs={"pk": 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))


class TestDeleteLabelView(LabelTestCase):
    def test_delete_label_view(self) -> None:
        """
        Test that the label delete confirmation view is accessible to an
            authenticated user.
        Verifies the response status and that the correct template is used.
        """
        response = self.client.get(
            reverse_lazy("label_delete", kwargs={"pk": 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, template_name="labels/delete_label.html"
        )

    def test_delete_label_not_logged_in_view(self) -> None:
        """
        Test that an unauthenticated user is redirected to the login page when
            attempting to access the label delete view.
        """
        self.client.logout()

        response = self.client.get(
            reverse_lazy("label_delete", kwargs={"pk": 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("login"))
