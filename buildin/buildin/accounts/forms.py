from django import forms
from django.contrib.auth import forms as auth_forms

from phone_field import PhoneField
from buildin.accounts.models import Profile

UserModel = auth_forms.get_user_model()


class UserRegistrationForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=Profile.FIRST_NAME_MAX_LENGTH)
    last_name = forms.CharField(max_length=Profile.LAST_NAME_MAX_LENGTH)
    role = forms.ChoiceField(choices=Profile.ROLES)

    class Meta:
        model = UserModel
        fields = ('email',)

    #saves Profile data of registered user
    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(first_name=self.cleaned_data['first_name'],
                          last_name=self.cleaned_data['last_name'],
                          participant_role=self.cleaned_data['role'],
                          user=user,)
        if commit:
            profile.save()
        return user
