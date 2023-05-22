from fastapi import HTTPException, status


def custom_response(status_code: status, details: str) -> HTTPException:
    """
    Returns a custom response with the given status code, details
    Parameters
    ----------
    status_code : The status code of the response
    details : The details of the response
    Returns
    -------
    HTPPException : The custom response
    """
    return HTTPException(status_code=status_code, detail=details)
