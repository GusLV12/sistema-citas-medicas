from rest_framework.exceptions import ValidationError

from config.exceptions import api_exception_handler


def test_validation_errors_keep_the_field_message():
    response = api_exception_handler(
        ValidationError({"slotId": ["El horario ya no es válido."]}),
        {},
    )

    assert response.status_code == 400
    assert response.data["message"] == "El horario ya no es válido."
    assert response.data["errors"] == {"slotId": ["El horario ya no es válido."]}
