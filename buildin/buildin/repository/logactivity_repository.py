from buildin.common.models import LogActivity


def create_logactivity_entity(user_id, action, model, to_related):
    LogActivity.objects.create(user_id=user_id, action=action, model=model, to_related=to_related)
