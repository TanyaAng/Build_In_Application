from django.db.models import signals
from django.dispatch import receiver

from buildin.core.helpers.crud_mapper import get_crud_mapper
from buildin.core.helpers.signals_helper import get_request_in_signal, get_signals_models_related
from buildin.core.repository.account_repository import get_request_user
from buildin.core.repository.logactivity_repository import create_logactivity_entity
from buildin.projects.models import BuildInProject


CRUD_MAPPER = get_crud_mapper()
MODELS_RELATED = get_signals_models_related()


@receiver(signals.post_save, sender=BuildInProject)
def project_created(instance, created, **kwargs):
    request = get_request_in_signal()
    user = get_request_user(request)
    action_create = f"{CRUD_MAPPER['CREATE']} {MODELS_RELATED['PROJECT']}"
    action_update = f"{CRUD_MAPPER['CREATE']} {MODELS_RELATED['PROJECT']}"
    model = instance.project_identifier
    to_related = MODELS_RELATED['APP']
    if created:
        create_logactivity_entity(user_email=user, action=action_create, model=model, to_related=to_related)



@receiver(signals.pre_delete, sender=BuildInProject)
def project_deleted(instance, **kwargs):
    request = get_request_in_signal()
    user = get_request_user(request)
    action = f"{CRUD_MAPPER['DELETE']} project"
    model = instance.project_identifier
    to_related = MODELS_RELATED['APP']
    create_logactivity_entity(user_email=user, action=action, model=model, to_related=to_related)
