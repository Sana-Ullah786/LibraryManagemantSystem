from fastapi import status


def custom_response(status_code: status, details: str, data: object = None) -> dict:
    """
    Returns a custom response with the given status code, details and data
    Parameters
    ----------
    status_code : The status code of the response
    details : The details of the response
    data : The data of the response
    Returns
    -------
    dict : The custom response
    """
    return {"status_code": status_code, "details": details, "data": data}
