from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import get_user_model

from phone_field import PhoneField

from buildin.accounts.models import Profile, BuildInUser

UserModel = get_user_model()


class CreateProfileForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=Profile.FIRST_NAME_MAX_LENGTH)
    last_name = forms.CharField(max_length=Profile.LAST_NAME_MAX_LENGTH)
    phone_number = PhoneField()
    participant_role = forms.ChoiceField(choices=Profile.ROLES)

    class Meta:
        model = UserModel
        fields = ('email', 'password1', 'password2')
