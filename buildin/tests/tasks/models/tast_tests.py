from factory.django import mute_signals
from django.db.models.signals import post_save

from django.test import TestCase

from buildin.accounts.models import BuildInUser
from buildin.projects.models import BuildInProject
from buildin.tasks.models import ProjectTask


class TaskModelTests(TestCase):

    def setUp(self) -> None:
        user_credentials = {
            'email': 'user@it.com',
            'password': '12345'
        }
        self.user = BuildInUser.objects.create_user(**user_credentials)
        self.client.login(**user_credentials)


    @mute_signals(post_save)
    def test_project__when_project_is_created__expect_to_has_slug_after_save(self):
        response = self.client.get("/my_profile/")
        user = response.context['user']

        project = BuildInProject(project_identifier='BG100', project_name='Apartament Hotel', owner=user)
        project.full_clean()
        project.save()

        task = ProjectTask(task_id='FP101', task_name='Formwork plan at level +3.00', project=project)
        task.full_clean()
        task.save()

        self.assertIsNotNone(task.slug)
