from django.db.models import signals
from django.dispatch import receiver

from buildin.core.helpers.signals_helper import get_request_in_signal
from buildin.projects.models import BuildInProject
from buildin.repository.account_repository import get_request_user_id
from buildin.repository.logactivity_repository import create_logactivity_entity

ACTION_CR_UP = 'create/update project'
ACTION_DEL = 'delete project'


@receiver(signals.post_save, sender=BuildInProject)
def project_created(instance, created, **kwargs):
    request = get_request_in_signal()
    user_id = get_request_user_id(request)
    action = ACTION_CR_UP
    model = instance.project_identifier
    to_related = 'database'
    if created:
        create_logactivity_entity(user_id, action, model, to_related)


@receiver(signals.post_delete, sender=BuildInProject)
def project_deleted(instance, created,  **kwargs):
    request = get_request_in_signal()
    user_id = get_request_user_id(request)
    action = ACTION_DEL
    model = instance.project_identifier
    to_related = 'database'
    if created:
        create_logactivity_entity(user_id, action, model, to_related)
