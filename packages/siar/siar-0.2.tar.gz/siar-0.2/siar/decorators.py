import json

def siar_exceptions(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        client = args[0]
        if client.exceptions_enabled and not response.ok:
            raise response.raise_for_status()

        return response
    return wrapper


def response_json(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)

        client = args[0]

        return response.json() if client.return_json else response
    return wrapper
