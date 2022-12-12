from buildin.projects.models import BuildInProject
from tests.utils.base_test_class import BaseTestCase
from django.urls import reverse

from django.db.models.signals import post_save
from factory.django import mute_signals


class ProjectEditViewTests(BaseTestCase):
    @mute_signals(post_save)
    def setUp(self) -> None:
        self.user, self.profile = self.create_login_and_make_profile_of_user()
        self.project = self.create_and_save_project_of_user(self.user)

    @mute_signals(post_save)
    def test_edit_project__when_user_try_to_access_project_where_not_owner__expect_to_be_forbidden(self):
        another_user_credentials = {
            'email': 'another_user@it.com',
            'password': '12345'
        }
        another_user = self.create_user_by_credentials(**another_user_credentials)
        another_project = self.create_and_save_project_of_user(another_user)

        response = self.client.get(reverse('project edit', kwargs={'build_slug': another_project.slug}))
        self.assertEqual(403, response.status_code)
