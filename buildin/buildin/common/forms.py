from django import forms

from buildin.common.models import TaskComment


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('description',)
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Add comment...', 'rows': '3'})
        }
