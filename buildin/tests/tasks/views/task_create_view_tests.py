from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.urls import reverse

from factory.django import mute_signals

from buildin.accounts.models import ParticipantRole, Profile
from buildin.projects.models import ProjectPhases, BuildInProject
from buildin.tasks.models import ProjectTask

UserModel = get_user_model()


class TaskCreateViewTests(TestCase):
    @mute_signals(post_save)
    def setUp(self) -> None:
        credentials = {
            'email': 'user@it.com',
            'password': '12345'
        }
        profile_info = {
            'first_name': 'Marina',
            'last_name': 'Petrova',
            'participant_role': ParticipantRole.choices()[3][0]
        }

        self.user = UserModel.objects.create_user(**credentials)
        self.client.login(**credentials)
        self.profile = Profile.objects.create(**profile_info, user=self.user)

        project_info = {
            'project_identifier': 'BG100',
            'project_name': 'Apartament Hotel',
            'project_phase': ProjectPhases.choices()[2][0],
            'client_name': 'Arch Studio Sofia',
            'deadline_date': '2023-05-06',
            'owner': self.user
        }

        self.project = BuildInProject(**project_info)
        self.project.full_clean()
        self.project.save()

    def test_create_task__expect_to_be_successfully_created(self):
        task = {
            'task_id': 'FP101',
            'task_name': 'Formwork plan at level +3.00',
        }
        response = self.client.post(reverse('task create', kwargs={'build_slug': self.project.slug}), data=task)
        task = ProjectTask.objects.filter(**task).get()
        self.assertIsNotNone(task)
        self.assertEqual(self.project, task.project)
        self.assertEqual(302, response.status_code)