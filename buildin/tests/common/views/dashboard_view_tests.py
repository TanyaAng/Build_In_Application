from tests.utils.base_test_class import BaseTestCase
from django.urls import reverse

from django.db.models.signals import post_save
from factory.django import mute_signals


class DashboardViewTest(BaseTestCase):
    def test_dashboard_view__when_no_authenticated_user__expect_redirect_to_login(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, '/accounts/login/')

    @mute_signals(post_save)
    def test_dashboard_view__when_is_authenticated_user__expect_to_render_own_dashboard(self):
        user = self.create_and_login_user()
        project_1 = self.create_and_save_project_of_user(user)


        another_user_credentials = {
            'email': 'another_user@it.com',
            'password': '12345'
        }
        another_user = self.create_user_by_credentials(**another_user_credentials)
        project_2 = self.create_and_save_project_of_user(another_user)


        response = self.client.get(reverse('dashboard'))
        self.assertEqual([project_1], list(response.context['projects']))
