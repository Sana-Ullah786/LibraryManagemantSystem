from fastapi import status


def custom_response(status_code: status, details: str, data: object = None) -> dict:
    """
    This function will be used to return a success response.
    Parameters:
        data: The data to be returned.
        details: The details of the response.
    Returns:
        A dictionary containing the response.
    """
    response = {"status_code": status_code, "data": data, "details": details}
    return response
