from django.test import TestCase

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.urls import reverse
from factory.django import mute_signals
from buildin.accounts.models import ParticipantRole, Profile
from buildin.projects.models import BuildInProject, ProjectPhases

UserModel = get_user_model()


class ProjectCreateViewTests(TestCase):
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

    @mute_signals(post_save)
    def test_create_project__expect_to_be_successfully_created(self):
        project_info = {
            'project_identifier': 'BG100',
            'project_name': 'Apartament Hotel',
            'project_phase': ProjectPhases.choices()[2][0],
            'client_name': 'Arch Studio Sofia',
            'deadline_date': '2023-05-06',
        }
        response = self.client.post(reverse('project create'), data=project_info)
        project = BuildInProject.objects.filter(**project_info).get()
        self.assertEqual(project_info['project_identifier'], project.project_identifier)
        self.assertEqual(project_info['project_name'], project.project_name)
        self.assertEqual(project_info['project_phase'], project.project_phase)
        self.assertEqual(project_info['client_name'], project.client_name)
        self.assertEqual(project_info['deadline_date'], str(project.deadline_date))
        self.assertEqual(self.user, project.owner)
        self.assertEqual(302, response.status_code)
