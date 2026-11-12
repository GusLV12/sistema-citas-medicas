from rest_framework.views import exception_handler


def _error_message(data):
    """Return the first useful validation message without dropping its context."""
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        return _error_message(data[0]) if data else None
    if isinstance(data, dict):
        if data.get("detail"):
            return _error_message(data["detail"])
        for value in data.values():
            message = _error_message(value)
            if message:
                return message
    return None


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response
    response.data = {
        "message": _error_message(response.data) or "No se pudo completar la solicitud.",
        "errors": response.data,
    }
    return response
