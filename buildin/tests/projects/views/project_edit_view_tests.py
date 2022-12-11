from django.db.models.signals import post_save
from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from factory.django import mute_signals

from buildin.accounts.models import ParticipantRole, Profile
from buildin.projects.models import ProjectPhases, BuildInProject

UserModel = get_user_model()


class ProjectEditViewTests(TestCase):
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
            'owner': self.user,
        }

        self.project = BuildInProject(**project_info)
        self.project.full_clean()
        self.project.save()

    @mute_signals(post_save)
    def test_edit_project__when_user_try_to_access_project_where_not_owner__expect_to_be_forbidden(self):
        second_user_credentials = {
            'email': 'second_user@it.com',
            'password': '12345'
        }
        second_user = UserModel.objects.create_user(**second_user_credentials)
        second_project = BuildInProject(project_identifier='BG200', project_name='Residential Building',
                                        owner=second_user)
        second_project.full_clean()
        second_project.save()

        response = self.client.get(reverse('project edit', kwargs={'build_slug': second_project.slug}))
        self.assertEqual(403, response.status_code)


    # def test_edit_project__when_user_access_own_project_or_participant__expect_to_update_data(self):
    #     update_project_info = {
    #         'project_identifier': 'BG100',
    #         'project_name': 'Residential Building',
    #         'project_phase': ProjectPhases.choices()[3][0],
    #         'client_name': 'Arch Studio Sofia',
    #         'deadline_date': '2023-10-06',
    #         'participants': UserModel.objects.all(),
    #     }
    #     # print(UserModel.objects.all())
    #     response = self.client.post(reverse('project edit', kwargs={'build_slug': self.project.slug}), data=update_project_info)
    #     project = BuildInProject.objects.filter(project_name=update_project_info['project_name']).get()
    #     self.assertEqual(self.project.pk, project.pk)
    #     self.assertEqual('Residential Building', project.project_name)
    #     self.assertEqual(ProjectPhases.choices()[3][0], project.project_phase)
    #     self.assertEqual('2023-10-06', str(project.deadline_date))
