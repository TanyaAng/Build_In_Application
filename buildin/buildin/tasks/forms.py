from django import forms
from django.contrib.auth import get_user_model
from buildin.tasks.models import ProjectTask

UserModel = get_user_model()


class CreateTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super().__init__(*args, **kwargs)

        self.participants = [p.email for p in self.project.participants.all()]
        self.fields['designer'].queryset = UserModel.objects.filter(email__in=self.participants)
        self.fields['checked_by'].queryset = UserModel.objects.filter(email__in=self.participants)

    class Meta:
        model = ProjectTask
        exclude = ('project', 'is_ready_for_markups', 'is_approved', 'is_issued')


class EditTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project')
        super().__init__(*args, **kwargs)

        self.participants = [p.email for p in self.project.participants.all()]
        self.fields['designer'].queryset = UserModel.objects.filter(email__in=self.participants)
        self.fields['checked_by'].queryset = UserModel.objects.filter(email__in=self.participants)

    class Meta:
        model = ProjectTask
        exclude = ('project',)
        widgets = {
            'is_ready_for_markups': forms.CheckboxInput(),
            'is_approved': forms.CheckboxInput(),
            'is_issued': forms.CheckboxInput(),
        }


class DeleteTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__hidden_fields()

    def __hidden_fields(self):
        for _, field in self.fields.items():
            field.widget = forms.HiddenInput()

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance

    class Meta:
        model = ProjectTask
        fields = '__all__'
