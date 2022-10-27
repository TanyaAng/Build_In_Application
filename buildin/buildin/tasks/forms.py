from django import forms

from buildin.tasks.models import ProjectTask


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        exclude = ('project',)


class EditTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        fields = '__all__'


class DeleteTaskForm(forms.ModelForm):
    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance

    class Meta:
        model = ProjectTask
        fields = '__all__'
