from fastapi import status
from fastapi.responses import JSONResponse


def custom_response(
    status_code: status, details: str, data: object = None
) -> JSONResponse:
    """
    Returns a custom response with the given status code, details and data
    Parameters
    ----------
    status_code : The status code of the response
    details : The details of the response
    data : The data of the response
    Returns
    -------
    A JSONResponse object
    """
    return JSONResponse(
        status_code=status_code, content={"details": details, "data": data}
    )
