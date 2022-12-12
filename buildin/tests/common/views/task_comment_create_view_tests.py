from buildin.common.models import TaskComment
from tests.utils.base_test_class import BaseTestCase

from django.db.models.signals import post_save
from factory.django import mute_signals

from django.urls import reverse


class TaskCommentCreateViewTests(BaseTestCase):

    @mute_signals(post_save)
    def test_task_comment_view__when_user_has_no_perm_to_this_project__expect_to_be_forbidden(self):
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

        response = self.client.get(reverse('comment section', kwargs={'task_slug': another_task.slug}))
        self.assertEqual(403, response.status_code)

    @mute_signals(post_save)
    def test_task_comment_view__when_user_has_perm_to_the_project__expect_to_render_all_comments_to_the_task(self):
        user = self.create_and_login_user()
        project = self.create_and_save_project_of_user(user)
        task = self.create_and_save_task_of_project(project)
        comment_1 = self.create_user_comment_to_task(task, user)

        response = self.client.get(reverse('comment section', kwargs={'task_slug': task.slug}))
        self.assertEqual(200, response.status_code)
        print(response.context['comments'])
        self.assertEqual([comment_1], list(response.context['comments']))

    @mute_signals(post_save)
    def test_task_comment_view__when_user_has_perm_to_the_project__expect_to_post_comment(self):
        user = self.create_and_login_user()
        project = self.create_and_save_project_of_user(user)
        task = self.create_and_save_task_of_project(project)

        comment_content = {
            'description': 'Add more details to the sections',
            'to_task': task,
            'user': user
        }

        response = self.client.post(reverse('comment section', kwargs={'task_slug': task.slug}), data=comment_content)
        comment = TaskComment.objects.all().first()
        self.assertRedirects(response, f'/comment/{task.slug}/')
        self.assertIsNotNone(comment)
