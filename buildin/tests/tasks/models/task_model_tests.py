from django.contrib.auth import get_user_model
from django.test import TestCase

from factory.django import mute_signals
from django.db.models.signals import post_save

from buildin.projects.models import BuildInProject
from buildin.tasks.models import ProjectTask

UserModel = get_user_model()


class TaskModelTests(TestCase):
    def setUp(self) -> None:
        credentials = {
            'email': 'user@it.com',
            'password': '12345'
        }
        self.user = UserModel.objects.create_user(**credentials)
        self.client.login(**credentials)

    @mute_signals(post_save)
    def test_project__when_project_is_created__expect_to_has_slug_after_save(self):
        project = BuildInProject(project_identifier='BG100', project_name='Apartament Hotel', owner=self.user)
        project.full_clean()
        project.save()

        task = ProjectTask(task_id='FP101', task_name='Formwork plan at level +3.00', project=project)
        task.full_clean()
        task.save()

        self.assertIsNotNone(task.slug)
