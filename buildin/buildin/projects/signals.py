from django.db.models import signals
from django.dispatch import receiver

from buildin.core.helpers.crud_mapper import get_crud_mapper
from buildin.core.helpers.signals_helper import get_request_in_signal, get_signals_models_related
from buildin.projects.models import BuildInProject
from buildin.repository.account_repository import get_request_user_id
from buildin.repository.logactivity_repository import create_logactivity_entity

CRUD_MAPPER = get_crud_mapper()
MODELS_RELATED = get_signals_models_related()

RELATED_PROJECTS_DB = 'Project repository'


@receiver(signals.post_save, sender=BuildInProject)
def project_created(instance, created, **kwargs):
    request = get_request_in_signal()
    user_id = get_request_user_id(request)
    action = f"{CRUD_MAPPER['CREATE']} {MODELS_RELATED['PROJECT']}"
    model = instance.project_identifier
    to_related = MODELS_RELATED['APP']
    if created:
        create_logactivity_entity(user_id=user_id, action=action, model=model, to_related=to_related)


@receiver(signals.pre_delete, sender=BuildInProject)
def project_deleted(instance, **kwargs):
    request = get_request_in_signal()
    user_id = get_request_user_id(request)
    action = f"{CRUD_MAPPER['DELETE']} project"
    model = instance.project_identifier
    to_related = RELATED_PROJECTS_DB
    create_logactivity_entity(user_id=user_id, action=action, model=model, to_related=to_related)
