from buildin.common.models import TaskComment


def get_all_comments_to_task(task):
    comments = TaskComment.objects.filter(to_task=task)
    return comments


def get_task_of_current_comment(comment):
    return comment.to_task


def get_task_id_of_current_comment(comment):
    return comment.to_task.pk


def get_owner_of_comment(comment):
    return comment.user
