from django import forms

from buildin.common.models import TaskComment


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('description',)
        labels = {
            'description': 'Comment:',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Add comment...', 'rows': '3'})
        }


class EditCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ('description',)
        labels = {
            'description': 'Comment:',
        }


class DeleteCommentForm(forms.ModelForm):
    class Meta:
        model = TaskComment
        fields = ()
