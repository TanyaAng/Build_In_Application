from django.db.models import signals
from django.dispatch import receiver

from buildin.common.models import TaskComment


@receiver(signals.post_save, sender=TaskComment)
def comment_created(instance, **kwargs):
    print(f"{instance.user} added new comment to {instance.to_task}.")
