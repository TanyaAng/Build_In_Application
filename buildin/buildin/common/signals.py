from django.db.models import signals
from django.dispatch import receiver

from buildin.common.models import TaskComment, LogActivity
from buildin.projects.models import BuildInProject


@receiver(signals.post_save, sender=TaskComment)
def comment_created(instance, **kwargs):
    user_id = instance.user.pk
    action = LogActivity.ACTION_CR_UP
    model = instance.to_task.task_id
    to_related = BuildInProject.objects.filter(projecttask__task_id=instance.to_task.task_id).get()
    LogActivity.objects.create(user_id=user_id, action=action, model=model, to_related=to_related)
    # print(f"{instance.user} added new comment to {instance.to_task}.")
