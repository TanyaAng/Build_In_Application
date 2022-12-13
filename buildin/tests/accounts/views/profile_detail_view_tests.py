from tests.utils.base_test_class import BaseTestCase

from factory.django import mute_signals
from django.db.models.signals import post_save

from django.urls import reverse

from buildin.projects.models import BuildInProject



class ProfileDetailViewTests(BaseTestCase):
    def setUp(self) -> None:
        self.user, self.profile = self.create_login_and_make_profile_of_user()

    def test_profile_details_view__when_user_try_to_access_another_user_profile_or_invalid_pk__expect_to_raise_not_found(self):
        response = self.client.get(reverse('profile details', kwargs={'pk': self.user.pk + 1}))
        self.assertEqual(response.status_code, self.HTTP_STATUS_NOT_FOUND)

    def test_profile_details_view__when_user_try_to_access_profile_page__expect_correct(self):
        response = self.client.get(reverse('profile details', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_OK)

    @mute_signals(post_save)
    def test_profile_details_view__when_user_access_profile_page__expect_correct_user_data(self):
        projects = self.create_and_save_multiple_projects_of_user(self.user)
        project = BuildInProject.objects.all().first()
        tasks = self.create_and_save_multiple_tasks_by_user_and_project(self.user, project)

        total_time_estimation = sum([t.time_estimation for t in tasks])

        response = self.client.get(reverse('profile details', kwargs={'pk': self.user.pk}))

        self.assertEqual(list(response.context['user_projects']), projects)
        self.assertEqual(list(response.context['user_designer_tasks']), tasks)
        self.assertEqual(response.context['total_time_of_tasks_to_design'], total_time_estimation)
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_OK)
