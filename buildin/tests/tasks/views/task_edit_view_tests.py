from tests.utils.base_test_class import BaseTestCase

from django.db.models.signals import post_save
from factory.django import mute_signals

from django.urls import reverse

from buildin.tasks.models import ProjectTask


class TaskCreateViewTests(BaseTestCase):
    @mute_signals(post_save)
    def setUp(self) -> None:
        self.user, self.profile = self.create_login_and_make_profile_of_user()

        self.project = self.create_and_save_project_of_user(self.user)

        self.task = self.create_and_save_task_of_project(self.project)

    @mute_signals(post_save)
    def test_edit_task__when_user_try_to_access_projecttask_where_not_participant__expect_to_be_forbidden(self):
        another_user_credentials = {
            'email': 'second_user@it.com',
            'password': '12345'
        }
        another_user = self.create_user_by_credentials(**another_user_credentials)
        another_project = self.create_and_save_project_of_user(another_user)
        another_task = self.create_and_save_task_of_project(another_project)

        response = self.client.get(
            reverse('task edit', kwargs={'build_slug': another_project.slug, 'task_slug': another_task.slug}))
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_FORBIDDEN)

    def test_edit_task__when_user_access_task__expect_to_update_data(self):
        update_task_name = 'Plan at level +6.00'
        update_task_info = {
            'task_id': self.task.task_id,
            'task_name': update_task_name,
        }
        response = self.client.post(
            reverse('task edit', kwargs={'build_slug': self.project.slug, 'task_slug': self.task.slug}),
            data=update_task_info)
        task = ProjectTask.objects.filter(**update_task_info).get()

        self.assertEqual(task.pk, self.task.pk)
        self.assertEqual(task.task_name, update_task_name)
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_FOUND)
