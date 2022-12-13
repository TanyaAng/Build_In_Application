from tests.utils.base_test_class import BaseTestCase

from django.db.models.signals import post_save
from factory.django import mute_signals

from django.urls import reverse

from buildin.common.models import TaskComment


class TaskCommentEditViewTests(BaseTestCase):

    @mute_signals(post_save)
    def test_task_comment_edit_view__when_user_is_not_owner_of_comment__expect_to_be_forbidden(self):
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
            reverse('comment edit', kwargs={'task_slug': another_task.slug, 'pk': another_comment.pk}))
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_FORBIDDEN)

    @mute_signals(post_save)
    def test_task_comment_edit_view__when_user_is_owner_of_comment__expect_to_update_comment(self):
        user = self.create_and_login_user()
        project = self.create_and_save_project_of_user(user)
        task = self.create_and_save_task_of_project(project)
        comment = self.create_user_comment_to_task(task=task, user=user)

        update_description = 'Add more details only for section 1'
        update_comment_content = {
            'description': update_description,
        }

        response = self.client.post(
            reverse('comment edit',
                    kwargs={'task_slug': task.slug, 'pk': comment.pk}),
            data=update_comment_content)

        update_comment = TaskComment.objects.get(**update_comment_content)

        self.assertEqual(comment.pk, update_comment.pk)
        self.assertEqual(update_description, update_comment.description)
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_FOUND)
