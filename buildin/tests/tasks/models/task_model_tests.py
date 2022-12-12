from tests.utils.base_test_class import BaseTestCase

from factory.django import mute_signals
from django.db.models.signals import post_save

from buildin.tasks.models import ProjectTask


class TaskModelTests(BaseTestCase):
    def setUp(self) -> None:
        self.user = self.create_and_login_user()

    @mute_signals(post_save)
    def test_project__when_project_is_created__expect_to_has_slug_after_save(self):
        project = self.create_and_save_project_of_user(self.user)

        task = ProjectTask(task_id='FP101', task_name='Plan at storey 3th', project=project)
        task.full_clean()
        task.save()

        self.assertIsNotNone(task.slug)
