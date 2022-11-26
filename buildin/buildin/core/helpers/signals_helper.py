import inspect


def get_request_in_signal():
    inspector = inspect.stack()
    for frame_record in inspector:
        if frame_record[3] == 'get_response':
            return frame_record[0].f_locals['request']
    return None


def get_signals_models_related():
    models = {
        'COMMENT': 'comment',
        'PROJECT': 'project',
        'TASK': 'task',
        'APP': 'application'
    }
    return models
