from tests.utils.base_test_class import BaseTestCase

from django.urls import reverse

from django.db.models.signals import post_save
from factory.django import mute_signals

from buildin.projects.models import BuildInProject, ProjectPhases


class ProjectCreateViewTests(BaseTestCase):
    def setUp(self) -> None:
        self.user, self.profile = self.create_login_and_make_profile_of_user()

    @mute_signals(post_save)
    def test_create_project__expect_to_be_successfully_created(self):
        project_info = {
            'project_identifier': 'BG100',
            'project_name': 'Hotel',
            'project_phase': ProjectPhases.choices()[2][0],
            'client_name': 'Arch Studio',
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
