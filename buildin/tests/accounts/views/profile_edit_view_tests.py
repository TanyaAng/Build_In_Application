from tests.utils.base_test_class import BaseTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from buildin.accounts.models import ParticipantRole, Profile

UserModel = get_user_model()


class ProfileEditViewTests(BaseTestCase):
    def setUp(self) -> None:
        self.user, self.profile = self.create_login_and_make_profile_of_user()

    def test_profile_edit__when_user_try_to_access_another_user_profile__expect_to_redirect(self):
        another_user_credentials = {
            'email': 'second_user@it.com',
            'password': '12345'
        }
        another_user_profile = {
            'first_name': 'George',
            'last_name': 'Ivanov',
            'participant_role': ParticipantRole.choices()[2][0]
        }
        another_user = self.create_user_by_credentials(**another_user_credentials)
        another_profile = self.create_profile_by_user_and_info(another_user, **another_user_profile)

        response = self.client.get(reverse('profile edit', kwargs={'pk': another_user.pk}))
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_FOUND)

    def test_profile_edit__when_user_try_to_access_own_profile__expect_to_be_successful(self):
        response = self.client.get(reverse('profile edit', kwargs={'pk': self.user.pk}))
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_OK)

    def test_profile_edit__when_some_data_has_changed__expect_to_update_data(self):
        update_last_name = 'Petrova - Marinova'
        update_participant_role = ParticipantRole.choices()[4][0]
        update_profile_info = {
            'first_name': self.profile.first_name,
            'last_name': update_last_name,
            'participant_role': update_participant_role
        }
        response = self.client.post(reverse('profile edit', kwargs={'pk': self.user.pk}), data=update_profile_info)
        profile = Profile.objects.filter(**update_profile_info).get()

        self.assertEqual(profile.pk, self.profile.pk,)
        self.assertEqual(profile.last_name ,update_last_name)
        self.assertEqual(profile.participant_role, update_participant_role)
        self.assertEqual(response.status_code, self.HTTP_STATUS_CODE_FOUND)
