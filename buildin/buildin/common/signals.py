from django.db.models import signals
from django.dispatch import receiver

from buildin.common.models import TaskComment, LogActivity
from buildin.repository.account_repository import get_request_user_id
from buildin.repository.common_repository import get_task_of_current_comment
from buildin.repository.logactivity_repository import create_logactivity_entity
from buildin.repository.project_repository import get_project_related_to_task


@receiver(signals.post_save, sender=TaskComment)
def comment_created(instance, **kwargs):
    user_id = get_request_user_id(instance)
    action = LogActivity.ACTION_CR_UP
    model = get_task_of_current_comment(instance)
    # TODO: to_related expect to return one object, it returns more than one
    to_related = get_project_related_to_task(task=model)
    create_logactivity_entity(user_id, action, model, to_related)
