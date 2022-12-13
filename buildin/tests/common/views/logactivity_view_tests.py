from tests.utils.base_test_class import BaseTestCase
from django.urls import reverse


class LogActivityViewTests(BaseTestCase):
    def test_logactivity_view__when_user_has_no_perm_to_the_view__expect_to_be_forbidden(self):
        user = self.create_and_login_user()
        response = self.client.get(reverse('log activity'))
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_FORBIDDEN)

    def test_logactivity_view__when_user_is_superuser__expect_render_successfully_log_activity(self):
        user = self.create_and_login_superuser()
        response = self.client.get(reverse('log activity'))
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_OK)

