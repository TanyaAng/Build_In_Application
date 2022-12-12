from tests.utils.base_test_class import BaseTestCase

from factory.django import mute_signals
from django.db.models.signals import post_save

from buildin.projects.models import BuildInProject


class BuildInProjectModelTests(BaseTestCase):
    def setUp(self) -> None:
        self.user = self.create_and_login_user()

    @mute_signals(post_save)
    def test_project__when_project_is_created__expect_to_has_slug_after_save(self):
        project = BuildInProject(project_identifier='BG100', project_name='Apartament Hotel', owner=self.user)
        project.full_clean()
        project.save()

        self.assertIsNotNone(project.slug)
