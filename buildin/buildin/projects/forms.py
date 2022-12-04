from django import forms

from buildin.core.repository.account_repository import get_users_by_profiles, get_profiles_of_participants

from buildin.projects.models import BuildInProject


class CreateProjectForm(forms.ModelForm):
    class Meta:
        model = BuildInProject
        exclude = ('participants', 'owner', 'date_added')
        labels = {
            'project_identifier': 'Project',
            'project_name': 'Project Name',
            'project_phase': 'Project Phase',
            'client_name': 'Contractor',
            'deadline_date': 'Deadline Date',
            'project_img': 'Image URL'
        }
        widgets = {
            'project_identifier': forms.TextInput(attrs={'placeholder': 'BG100 - NEW ARCH - BUILDING A'}),
            'project_name': forms.TextInput(attrs={'placeholder': 'Residential Building in Sofia'}),
            'client_name': forms.TextInput(attrs={'placeholder': 'New Arch'}),
            'project_img': forms.TextInput(attrs={'placeholder': 'Link to Image'}),
            'deadline_date': forms.TextInput(attrs={'type': 'date'}),
        }


class EditProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__get_participants_profile()

    def __get_participants_profile(self):
        participants = self.fields.get('participants').queryset
        self.fields['participants'].queryset = get_profiles_of_participants(participants)

    def clean_participants(self):
        participants_profile = self.cleaned_data['participants']
        users = get_users_by_profiles(participants_profile)
        self.fields['participants'].queryset = users
        self.cleaned_data['participants'] = users
        return self.cleaned_data['participants']

    class Meta:
        model = BuildInProject
        exclude = ('date_added', 'owner',)
        labels = {
            'project_identifier': 'Project',
            'project_name': 'Project Name',
            'project_phase': 'Project Phase',
            'client_name': 'Contractor',
            'deadline_date': 'Deadline Date',
            'project_img': 'Image URL'
        }
        widgets = {
            'project_name': forms.TextInput(),
            'participants': forms.CheckboxSelectMultiple(),
        }


class DeleteProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__readonly_fields()

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance

    def __readonly_fields(self):
        for _, field in self.fields.items():
            field.widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = BuildInProject
        exclude = ('participants', 'project_img', 'date_added', 'owner')
        widgets = {
            'project_name': forms.TextInput(),
        }
