from django.db.models import signals
from django.dispatch import receiver

from buildin.common.models import LogActivity
from buildin.core.helpers.signals_helper import get_request_in_signal
from buildin.tasks.models import ProjectTask

ACTION_CR_UP = 'create/update project'
ACTION_DEL = 'delete project'

@receiver(signals.post_save, sender=ProjectTask)
def task_created(instance, **kwargs):
    request = get_request_in_signal()
    user_id = request.user.pk
    action = ACTION_CR_UP
    model = instance.task_id
    to_related = instance.project
    LogActivity.objects.create(user_id=user_id, action=action, model=model, to_related=to_related)
    # print(f"{request.user} saves to db a new task {instance.task_id} to project {instance.project}!")


@receiver(signals.post_delete, sender=ProjectTask)
def task_deleted(instance, **kwargs):
    request = get_request_in_signal()
    user_id = request.user.pk
    action = ACTION_CR_UP
    model = instance.task_id
    to_related = instance.project
    LogActivity.objects.create(user_id=user_id, action=action, model=model, to_related=to_related)
    # print(f"{request.user} deleted a task {instance.task_id} from project {instance.project}!")
