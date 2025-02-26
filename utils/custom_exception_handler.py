from rest_framework.views import exception_handler  # Default DRF exception handler
from rest_framework import status  # DRF HTTP status codes
from http import HTTPStatus  # Standard HTTP status codes
from rest_framework.response import Response  # DRF Response object

def custom_exception_handler(exc, context):
    """
    Custom Exception Handler for Django REST Framework (DRF).
    
    - It first calls DRF's default `exception_handler()`, which processes known exceptions.
    - If a response is generated, we modify its structure.
    - If no response is returned (for unhandled errors), we create a generic error response.
    """

    # Call the default DRF exception handler first
    response = exception_handler(exc, context)

    # Standard HTTP Status Messages (e.g., {404: "Not Found", 500: "Internal Server Error"})
    http_code_to_message = {v.value: v.description for v in HTTPStatus}

    # Define a structured JSON error response format
    error_payload = {
        "error": {
            "status_code": 0,  # Placeholder for status code
            "message": "",  # Placeholder for error message
            "details": []  # Placeholder for error details
        }
    }
    error = error_payload["error"]  # Shortcut to access the `error` dictionary

    # If DRF handled the exception (e.g., 404 Not Found, 400 Bad Request)
    if response is not None:
        status_code = response.status_code  # Extract HTTP status code

        error["status_code"] = status_code  # Set the error status code
        error["message"] = http_code_to_message.get(status_code, "Unknown Error")  # Get standard message
        error["details"] = response.data  # Include DRF’s default error details

        response.data = error_payload  # Replace response data with our structured error
        return response  # Return the modified response

    # If an **unexpected** error occurs (e.g., database crash, unhandled exceptions)
    else:
        error["status_code"] = status.HTTP_500_INTERNAL_SERVER_ERROR  # Default to 500
        error["message"] = "Internal Server Error"  # Standard 500 error message
        error["details"] = [str(exc)]  # Convert Python exception to a string and include in details

        return Response(error_payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
