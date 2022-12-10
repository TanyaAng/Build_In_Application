from factory.django import mute_signals
from django.db.models.signals import post_save

from django.test import TestCase

from buildin.accounts.models import BuildInUser
from buildin.projects.models import BuildInProject


class BuildInProjectModelTests(TestCase):

    def setUp(self) -> None:
        user_credentials = {
            'email': 'user@it.com',
            'password': '12345'
        }
        self.user = BuildInUser.objects.create_user(**user_credentials)
        self.client.login(username='user@it.com', password='12345')

    @mute_signals(post_save)
    def test_project__when_project_is_created__expect_to_has_slug_after_save(self):
        response = self.client.get("/my_profile/")
        user = response.context['user']

        project = BuildInProject(project_identifier='BG100', project_name='Apartament Hotel', owner=user)
        project.full_clean()
        project.save()

        self.assertIsNotNone(project.slug)
