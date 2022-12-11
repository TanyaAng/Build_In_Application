from django.test import TestCase

from django.db.models.signals import post_save

from django.contrib.auth import get_user_model
from django.urls import reverse
from factory.django import mute_signals

from buildin.accounts.models import ParticipantRole, Profile
from buildin.projects.models import ProjectPhases, BuildInProject

UserModel = get_user_model()


class ProjectDetailViewTests(TestCase):
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

    def test_project_details_page__expect_to_have_correct_project_data(self):
        response = self.client.get(reverse('project details', kwargs={'build_slug': self.project.slug}))

        self.assertEqual(response.context['project'], self.project)
