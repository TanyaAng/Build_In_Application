from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from buildin.accounts.models import ParticipantRole, Profile

UserModel = get_user_model()


class ProfileEditViewTests(TestCase):
    def setUp(self) -> None:
        credentials = {
            'email': 'user@it.com',
            'password': '12345'
        }
        profile_info = {
            'first_name': 'Marina',
            'last_name': 'Petrova',
            'participant_role': ParticipantRole.choices()[3][0]
        }

        self.user = UserModel.objects.create_user(**credentials)
        self.client.login(**credentials)
        self.profile = Profile.objects.create(**profile_info, user=self.user)

    def test_profile_edit__when_user_try_to_access_another_user_profile__expect_to_redirect(self):
        credentials = {
            'email': 'second_user@it.com',
            'password': '12345'
        }
        profile_info = {
            'first_name': 'George',
            'last_name': 'Marinov',
            'participant_role': ParticipantRole.choices()[2][0]
        }
        user = UserModel.objects.create_user(**credentials)
        Profile.objects.create(**profile_info, user=user)

        response = self.client.get(reverse('profile edit', kwargs={'pk': user.pk}))
        self.assertEqual(302, response.status_code)

    def test_profile_edit__when_user_try_to_access_own_profile__expect_to_be_successful(self):
        response = self.client.get(reverse('profile edit', kwargs={'pk': self.user.pk}))
        self.assertEqual(200, response.status_code)

    def test_profile_edit__when_some_data_has_changed__expect_to_update_data(self):
        update_profile_info = {
            'first_name': 'Marina',
            'last_name': 'Petrova - Marinova',
            'participant_role': ParticipantRole.choices()[4][0]
        }
        response = self.client.post(reverse('profile edit', kwargs={'pk': self.user.pk}), data=update_profile_info)
        profile = Profile.objects.filter(**update_profile_info).get()
        self.assertEqual(self.profile.pk, profile.pk)
        self.assertEqual('Petrova - Marinova', profile.last_name)
        self.assertEqual(302, response.status_code)
