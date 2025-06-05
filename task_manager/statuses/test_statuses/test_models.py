from django.utils import timezone

from task_manager.statuses.models import Status
from .testcase import StatusTestCase


class StatusModelTest(StatusTestCase):
    def test_status_creation(self) -> None:
        """
        Test that a new status can be successfully created with valid data.
        Verifies the instance type, string representation, and field values.
        """
        status_data = self.test_status["create"]["valid"].copy()

        status, created = Status.objects.get_or_create(
            name=status_data["name"], created_at=timezone.now()
        )

        self.assertTrue(isinstance(status, Status))
        self.assertEqual(status.__str__(), status_data["name"])
        self.assertEqual(status.name, status_data["name"])
