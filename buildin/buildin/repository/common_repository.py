from buildin.common.models import TaskComment


def get_all_comments_to_task(task):
    comments = TaskComment.objects.filter(to_task=task)
    return comments


def get_task_id_of_current_comment(task_comment):
    return task_comment.to_task.pk

def get_task_of_current_comment(task_comment):
    return task_comment.to_task