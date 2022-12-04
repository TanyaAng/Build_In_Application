from django.db.models import signals
from django.dispatch import receiver

from buildin.common.models import TaskComment
from buildin.core.helpers.crud_mapper import get_crud_mapper
from buildin.core.helpers.signals_helper import get_signals_models_related, get_request_in_signal
from buildin.core.repository.account_repository import get_request_user
from buildin.core.repository.common_repository import get_task_of_current_comment
from buildin.core.repository.logactivity_repository import create_logactivity_entity

from buildin.core.repository.project_repository import get_project_related_to_task

CRUD_MAPPER = get_crud_mapper()
MODELS_RELATED = get_signals_models_related()


@receiver(signals.post_save, sender=TaskComment)
def comment_created(instance, **kwargs):
    user = get_request_user(instance)
    model = get_task_of_current_comment(instance)
    action = f"{CRUD_MAPPER['CREATE']} {MODELS_RELATED['COMMENT']}"
    to_related = get_project_related_to_task(task=model)
    create_logactivity_entity(user_email=user, action=action,
                              model=model, to_related=to_related)


@receiver(signals.pre_delete, sender=TaskComment)
def comment_deleted(instance, **kwargs):
    request = get_request_in_signal()
    user = get_request_user(request)
    model = get_task_of_current_comment(instance)
    action = f"{CRUD_MAPPER['DELETE']} {MODELS_RELATED['COMMENT']}"
    to_related = get_project_related_to_task(task=model)
    create_logactivity_entity(user_email=user, action=action,
                              model=model, to_related=to_related)
