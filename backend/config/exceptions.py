from rest_framework.views import exception_handler

def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return response
    detail = response.data.get("detail") if isinstance(response.data, dict) else None
    response.data = {"message": str(detail or "No se pudo completar la solicitud."), "errors": response.data}
    return response
