import inspect


def get_request_in_signal():
    inspector = inspect.stack()
    for frame_record in inspector:
        if frame_record[3] == 'get_response':
            return frame_record[0].f_locals['request']
    return None
