from tests.utils.base_test_class import BaseTestCase
from django.urls import reverse


class HomeViewTests(BaseTestCase):
    def test_home_view__when_is_authenticated_user__expect_to_redirect_to_dashboard_view(self):
        self.create_and_login_user()
        response = self.client.get(reverse('home page'))

        self.assertRedirects(response, '/dashboard/')
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_FOUND)

    def test_home_view__when_is_not_authenticated_user__expect_to_render_home_view(self):
        response = self.client.get(reverse('home page'))
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_OK)
