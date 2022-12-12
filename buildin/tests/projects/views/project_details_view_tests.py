from tests.utils.base_test_class import BaseTestCase

from django.db.models.signals import post_save
from factory.django import mute_signals

from django.urls import reverse


class ProjectDetailViewTests(BaseTestCase):
    @mute_signals(post_save)
    def setUp(self) -> None:
        self.user, self.profile = self.create_login_and_make_profile_of_user()
        self.project = self.create_and_save_project_of_user(self.user)

    @mute_signals(post_save)
    def test_project_details__when_user_try_to_access_project_where_not_owner_or_participant__expect_to_be_forbidden(self):
        another_user_credentials = {
            'email': 'another_user@it.com',
            'password': '12345'
        }
        another_user = self.create_user_by_credentials(**another_user_credentials)
        another_project = self.create_and_save_project_of_user(another_user)

        response = self.client.get(reverse('project details', kwargs={'build_slug': another_project.slug}))
        self.assertEqual(403, response.status_code)

    def test_project_details_page__expect_to_have_correct_project_data(self):
        response = self.client.get(reverse('project details', kwargs={'build_slug': self.project.slug}))
        self.assertEqual(response.context['project'], self.project)
