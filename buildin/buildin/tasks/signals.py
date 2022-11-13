from django.db.models import signals
from django.dispatch import receiver

from buildin.core.helpers.signals_helper import get_request_in_signal
from buildin.tasks.models import ProjectTask


@receiver(signals.post_save, sender=ProjectTask)
def task_created(instance, **kwargs):
    request = get_request_in_signal()
    print(f"{request.user} saves to db a new task {instance.task_id} to project {instance.project}!")


@receiver(signals.post_delete, sender=ProjectTask)
def task_deleted(instance, **kwargs):
    request = get_request_in_signal()
    print(f"{request.user} deleted a task {instance.task_id} from project {instance.project}!")
