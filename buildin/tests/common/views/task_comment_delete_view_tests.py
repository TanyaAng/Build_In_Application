from tests.utils.base_test_class import BaseTestCase

from django.db.models.signals import post_save, pre_delete
from factory.django import mute_signals

from django.urls import reverse

from buildin.common.models import TaskComment


class TaskCommentDeleteViewTests(BaseTestCase):

    @mute_signals(post_save)
    def test_task_comment_delete_view__when_user_is_not_owner_of_comment__expect_to_be_forbidden(self):
        user = self.create_and_login_user()
        project = self.create_and_save_project_of_user(user)
        task = self.create_and_save_task_of_project(project)

        another_user_credentials = {
            'email': 'another_user@it.com',
            'password': '12345'
        }
        another_user = self.create_user_by_credentials(**another_user_credentials)
        another_project = self.create_and_save_project_of_user(another_user)
        another_task = self.create_and_save_task_of_project(another_project)
        another_comment = self.create_user_comment_to_task(task=another_task, user=another_user)

        response = self.client.get(
            reverse('comment delete', kwargs={'task_slug': another_task.slug, 'pk': another_comment.pk}))
        self.assertEqual(403, response.status_code)

    @mute_signals(post_save, pre_delete)
    def test_task_comment_delete_view__when_user_is_owner_of_comment__expect_to_delete_comment(self):
        user = self.create_and_login_user()
        project = self.create_and_save_project_of_user(user)
        task = self.create_and_save_task_of_project(project)
        comment = self.create_user_comment_to_task(task=task, user=user)

        response = self.client.post(
            reverse('comment delete',
                    kwargs={'task_slug': task.slug, 'pk': comment.pk}),
        )

        comment = TaskComment.objects.all()

        self.assertEqual([], list(comment))
