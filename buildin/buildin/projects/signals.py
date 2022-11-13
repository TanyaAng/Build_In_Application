from django.db.models import signals
from django.dispatch import receiver

from buildin.core.helpers.signals_helper import get_request_in_signal
from buildin.projects.models import BuildInProject


@receiver(signals.post_save, sender=BuildInProject)
def project_created(instance, **kwargs):
    request = get_request_in_signal()
    print(f"{request.user} saves to db a new project {instance.project_identifier}!")


@receiver(signals.post_delete, sender=BuildInProject)
def project_deleted(instance, **kwargs):
    request = get_request_in_signal()
    print(f"{request.user} delete a project {instance.project_identifier} from DB!")
