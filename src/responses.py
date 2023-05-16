from fastapi import status


def success_response(data: object = None, details: str = "Succes") -> dict:
    """
    This function will be used to return a success response.
    Parameters:
        data: The data to be returned.
        details: The details of the response.
    Returns:
        A dictionary containing the response.
    """
    response = {"status_code": status.HTTP_200_OK, "data": data, "details": details}
    return response


def error_response(
    status: status = None, data: object = None, details: str = "Error"
) -> dict:
    """
    This function will be used to return an error response.
    Parameters:
        status: The status code of the response.
        details: The details of the response.
    Returns:
        A dictionary containing the response.
    """
    response = {"status_code": status, "data": data, "details": details}
    return response
