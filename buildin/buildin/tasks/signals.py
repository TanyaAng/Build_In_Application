from django.db.models import signals
from django.dispatch import receiver

from buildin.core.helpers.crud_mapper import get_crud_mapper
from buildin.core.helpers.signals_helper import get_request_in_signal, get_signals_models_related
from buildin.repository.account_repository import get_request_user_id
from buildin.repository.logactivity_repository import create_logactivity_entity
from buildin.repository.project_repository import get_project_related_to_task
from buildin.tasks.models import ProjectTask

CRUD_MAPPER = get_crud_mapper()
MODELS_RELATED = get_signals_models_related()


@receiver(signals.post_save, sender=ProjectTask, dispatch_uid='unique_identifier')
def task_created(instance, created, **kwargs):
    request = get_request_in_signal()
    user = get_request_user_id(request)
    action = f"{CRUD_MAPPER['CREATE']} {MODELS_RELATED['TASK']}"
    model = instance
    to_related = get_project_related_to_task(instance)
    print(f"Created: {created}\nSlug: {instance.slug}")
    if created:
        create_logactivity_entity(user_email=user, action=action, model=model, to_related=to_related)


@receiver(signals.pre_delete, sender=ProjectTask)
def task_deleted(instance, **kwargs):
    request = get_request_in_signal()
    user = get_request_user_id(request)
    action = f"{CRUD_MAPPER['DELETE']} {MODELS_RELATED['TASK']}"
    model = instance
    to_related = get_project_related_to_task(instance)
    create_logactivity_entity(user_email=user, action=action, model=model, to_related=to_related)
