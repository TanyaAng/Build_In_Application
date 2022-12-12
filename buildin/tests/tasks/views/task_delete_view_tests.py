from tests.utils.base_test_class import BaseTestCase

from django.db.models.signals import post_save, pre_delete
from factory.django import mute_signals

from django.urls import reverse

from buildin.tasks.models import ProjectTask


class TaskDeleteViewTests(BaseTestCase):
    @mute_signals(post_save)
    def setUp(self) -> None:
        self.user, self.profile = self.create_login_and_make_profile_of_user()
        self.project = self.create_and_save_project_of_user(self.user)

        self.task = self.create_and_save_task_of_project(self.project)

    @mute_signals(post_save)
    def test_delete_task__when_user_try_to_access_projecttask_where_not_participant__expect_to_be_forbidden(self):
        another_user_credentials = {
            'email': 'another_user@it.com',
            'password': '12345'
        }
        another_user = self.create_user_by_credentials(**another_user_credentials)
        another_project = self.create_and_save_project_of_user(another_user)
        another_task = self.create_and_save_task_of_project(another_project)

        response = self.client.get(
            reverse('task delete', kwargs={'build_slug': another_project.slug, 'task_slug': another_task.slug}))
        self.assertEqual(403, response.status_code)

    # @mute_signals(post_save,pre_delete)
    # def test_delete_task__when_user_to_access_task_where_is_participant_or_owner__expect_delete_task(self):
    #     task_content = {}
    #     for key, value in self.task.__dict__.items():
    #         if value:
    #             task_content[key] = value
    #     print(task_content)
    #
    #     response = self.client.post(
    #         reverse('task delete', kwargs={'build_slug': self.project.slug, 'task_slug': self.task.slug}))
    #     tasks = ProjectTask.objects.all()
    #     self.assertEqual([], list(tasks))
