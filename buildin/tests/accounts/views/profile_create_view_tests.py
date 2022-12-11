from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from buildin.accounts.models import Profile, ParticipantRole

UserModel = get_user_model()


class ProfileCreateViewTests(TestCase):
    def setUp(self) -> None:
        credentials = {
            'email': 'user@it.com',
            'password': '12345'
        }

        self.user = UserModel.objects.create_user(**credentials)
        self.client.login(**credentials)

    def test_profile_create__when_logged_user_creates_profile__expect_correct_creation_one_to_one_relation(self):
        profile_info = {
            'first_name': 'Marina',
            'last_name': 'Petrova',
            'participant_role': ParticipantRole.choices()[3][0],
            'user': self.user
        }
        response = self.client.post(reverse('profile create'), data=profile_info)
        profile=Profile.objects.filter(**profile_info).get()
        self.assertIsNotNone(profile)
        self.assertEqual(302, response.status_code)
        self.assertEqual(self.user.pk, profile.pk)

