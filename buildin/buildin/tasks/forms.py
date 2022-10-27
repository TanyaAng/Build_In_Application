from django import forms

from buildin.tasks.models import ProjectTask


class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = ProjectTask
        exclude = ('project', 'is_ready_for_markups', 'is_approved', 'is_issued')


class EditTaskForm(forms.ModelForm):
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
