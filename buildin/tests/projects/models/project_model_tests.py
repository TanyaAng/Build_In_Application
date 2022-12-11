from django.test import TestCase

from django.contrib.auth import get_user_model
from factory.django import mute_signals
from django.db.models.signals import post_save

from buildin.projects.models import BuildInProject

UserModel = get_user_model()


class BuildInProjectModelTests(TestCase):
    def setUp(self) -> None:
        credentials = {
            'email': 'user@it.com',
            'password': '12345'
        }
        self.user = UserModel.objects.create_user(**credentials)
        self.client.login(**credentials)

    @mute_signals(post_save)
    def test_project__when_project_is_created__expect_to_has_slug_after_save(self):
        project = BuildInProject(project_identifier='BG100', project_name='Apartament Hotel', owner=self.user)
        project.full_clean()
        project.save()

        self.assertIsNotNone(project.slug)


