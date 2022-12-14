from buildin.projects.models import BuildInProject
from tests.utils.base_test_class import BaseTestCase

from django.db.models.signals import post_save, pre_delete
from factory.django import mute_signals

from django.urls import reverse


class ProjectDeleteViewTests(BaseTestCase):
    @mute_signals(post_save)
    def setUp(self) -> None:
        self.user, self.profile = self.create_login_and_make_profile_of_user()
        self.project = self.create_and_save_project_of_user(self.user)

    @mute_signals(post_save)
    def test_delete_project__when_user_try_to_access_project_where_not_owner_or_participant__expect_to_be_forbidden(
            self):
        another_user_credentials = {
            'email': 'another_user@it.com',
            'password': '12345'
        }
        another_user = self.create_user_by_credentials(**another_user_credentials)
        another_project = self.create_and_save_project_of_user(another_user)

        response = self.client.get(reverse('project delete', kwargs={'build_slug': another_project.slug}))
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_FORBIDDEN)

    @mute_signals(post_save, pre_delete)
    def test_delete_project__when_user_try_to_access_project_where_is_owner_or_participant__expect_delete_project(
            self):
        project_content = {}

        for key, value in self.project.__dict__.items():
            if value:
                project_content[key] = value

        response = self.client.post(reverse('project delete', kwargs={'build_slug': self.project.slug}),
                                    data=project_content)
        project = BuildInProject.objects.all()

        self.assertEqual(list(project), [])
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_FOUND)
