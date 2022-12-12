from tests.utils.base_test_class import BaseTestCase

from django.db.models.signals import post_save
from factory.django import mute_signals

from django.urls import reverse

from buildin.tasks.models import ProjectTask


class TaskCreateViewTests(BaseTestCase):
    @mute_signals(post_save)
    def setUp(self) -> None:
        self.user, self.profile = self.create_login_and_make_profile_of_user()

        self.project = self.create_and_save_project_of_user(self.user)

    def test_create_task__expect_to_be_successfully_created(self):
        task = {
            'task_id': 'FP101',
            'task_name': 'Plan at storey 3th',
        }
        response = self.client.post(reverse('task create', kwargs={'build_slug': self.project.slug}), data=task)
        task = ProjectTask.objects.filter(**task).get()
        self.assertIsNotNone(task)
        self.assertEqual(self.project, task.project)
        self.assertEqual(302, response.status_code)
