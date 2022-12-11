from django.contrib.auth import get_user_model
from django.test import TestCase
from factory.django import mute_signals
from django.db.models.signals import post_save

from django.urls import reverse

from buildin.accounts.models import ParticipantRole, Profile
from buildin.projects.models import BuildInProject
from buildin.tasks.models import ProjectTask

UserModel = get_user_model()


class ProfileDetailViewTests(TestCase):
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

    def test_profile_details_view__when_user_try_to_access_another_user_profile__expect_to_redirect(self):
        response = self.client.get(reverse('profile details', kwargs={'pk': self.user.pk + 1}))
        self.assertEqual(response.status_code, 302)

    def test_profile_details_view__when_user_try_to_access_profile_page__expect_correct(self):
        response = self.client.get(reverse('profile details', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, 200)

    @mute_signals(post_save)
    def test_profile_details_view__when_user_access_profile_page__expect_correct_user_data(self):
        projects = []
        for i in range(1, 10):
            project = BuildInProject(
                project_identifier=100 + i,
                project_name=f'Residential Building on {i}th street',
                owner=self.user,
            )
            project.full_clean()
            project.save()
            projects.append(project)

        tasks = []
        for i in range(1, 3):
            task = ProjectTask(
                task_id=f'FP{100 + i}',
                task_name=f'Plan for storey {i}',
                time_estimation=i,
                designer=self.user,
                project=BuildInProject.objects.get(pk=1),
            )
            task.full_clean()
            task.save()
            tasks.append(task)

        total_time_estimation = sum([t.time_estimation for t in tasks])

        response = self.client.get(reverse('profile details', kwargs={'pk': self.user.pk}))

        self.assertEqual(list(response.context['user_projects']), projects)
        self.assertEqual(list(response.context['user_designer_tasks']), tasks)
        self.assertEqual(response.context['total_time_of_tasks_to_design'], total_time_estimation)
