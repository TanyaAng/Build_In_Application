from django.db.models import signals
from django.dispatch import receiver

from buildin.core.helpers.signals_helper import get_request_in_signal
from buildin.repository.account_repository import get_request_user_id
from buildin.repository.logactivity_repository import create_logactivity_entity
from buildin.repository.project_repository import get_project_related_to_task
from buildin.tasks.models import ProjectTask

ACTION_CR_UP = 'create/update project'
ACTION_DEL = 'delete project'

@receiver(signals.post_save, sender=ProjectTask)
def task_created(instance, created, **kwargs):
    print(created)
    request = get_request_in_signal()
    user_id = get_request_user_id(request)
    action = ACTION_CR_UP
    model = instance
    to_related = get_project_related_to_task(instance)
    if created:
        create_logactivity_entity(user_id, action, model, to_related)



@receiver(signals.post_delete, sender=ProjectTask)
def task_deleted(instance, created, **kwargs):
    request = get_request_in_signal()
    user_id = get_request_user_id(request)
    action = ACTION_CR_UP
    model = instance
    to_related = get_project_related_to_task(instance)
    if created:
        create_logactivity_entity(user_id, action, model, to_related)

