from django import forms
from django.contrib.auth import forms as auth_forms

from buildin.accounts.models import Profile, ParticipantRole

UserModel = auth_forms.get_user_model()


class UserRegistrationForm(auth_forms.UserCreationForm):
    first_name = forms.CharField(max_length=Profile.FIRST_NAME_MAX_LENGTH)
    last_name = forms.CharField(max_length=Profile.LAST_NAME_MAX_LENGTH)
    role = forms.ChoiceField(choices=ParticipantRole.choices())

    class Meta:
        model = UserModel
        fields = ('email',)

    # saves Profile data of registered user
    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile(first_name=self.cleaned_data['first_name'],
                          last_name=self.cleaned_data['last_name'],
                          participant_role=self.cleaned_data['role'],
                          user=user, )
        if commit:
            profile.save()
        return user


class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)
        widgets = {
            'phone_number_1': forms.CharField(widget=forms.HiddenInput(), required=False)
        }


class EditProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__hidden_phone_input()

    def __hidden_phone_input(self):
        self.fields['phone_number'].fields[1].widget.attrs.update({'class': 'id_phone_number_100'})

    class Meta:
        model = Profile
        exclude = ('user',)
