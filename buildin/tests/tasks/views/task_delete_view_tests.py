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

        task_info = {
            'task_id': 'FP101',
            'task_name': 'Formwork plan at level +3.00',
            'project': self.project,
        }
        self.task = ProjectTask(**task_info)
        self.task.full_clean()
        self.task.save()

    @mute_signals(post_save)
    def test_delete_task__when_user_try_to_access_projecttask_where_not_participant__expect_to_be_forbidden(self):
        second_user_credentials = {
            'email': 'second_user@it.com',
            'password': '12345'
        }
        second_user = UserModel.objects.create_user(**second_user_credentials)
        second_project = BuildInProject(project_identifier='BG200', project_name='Residential Building',
                                        owner=second_user)
        second_project.full_clean()
        second_project.save()
        second_task_info = {
            'task_id': 'FP200',
            'task_name': 'Plan at level +6.00',
            'project': second_project
        }
        second_task = ProjectTask(**second_task_info)
        second_task.full_clean()
        second_task.save()

        response = self.client.post(
            reverse('task delete', kwargs={'build_slug': second_project.slug, 'task_slug': second_task.slug}),
            data=second_task_info)
        self.assertEqual(403, response.status_code)



