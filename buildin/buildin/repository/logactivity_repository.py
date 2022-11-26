from buildin.common.models import LogActivity


def create_logactivity_entity(user_email, action, model, to_related):
    LogActivity.objects.create(user=user_email, action=action, model=model, to_related=to_related)
