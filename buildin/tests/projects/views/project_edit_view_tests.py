
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

    # def test_edit_project__when_user_access_own_project_or_participant__expect_to_update_data(self):
    #     update_project_name = 'Residential Building'
    #     update_project_client = 'Stroi LTD'
    #     update_project_deadline = '2023-08-10'
    #     update_project_info = {
    #         'project_identifier': self.project.project_identifier,
    #         'project_name': update_project_name,
    #         'project_phase': self.project.project_phase,
    #         'client_name': update_project_client,
    #         'deadline_date': update_project_deadline,
    #         'owner': self.user,
    #         'participants': self.user,
    #     }
    #
    #     response = self.client.post(reverse('project edit', kwargs={'build_slug': self.project.slug}),
    #                                 data=update_project_info)
    #     project = BuildInProject.objects.filter(project_name=update_project_info['project_name']).get()
    #     self.assertEqual(self.project.pk, project.pk)
    #     self.assertEqual(update_project_name, project.project_name)
    #     self.assertEqual(update_project_client, project.client_name)
    #     self.assertEqual(update_project_deadline, str(project.deadline_date))
