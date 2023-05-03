from fastapi import HTTPException
from starlette import status


def db_not_available() -> HTTPException:
    """
    Custom exception that can be raised if query execution fails.\n
    Returns
    -------
    Custom HTTPException object
    """
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database is down. Try again later.",
    )


def user_not_exist() -> HTTPException:
    """
    Custom exception that can be raised user does not exist.\n
    Returns
    -------
    Custom HTTPException object
    """
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No such user exists",
    )


def invalid_data() -> HTTPException:
    """
    Custom exception that can be raised while updating user\n
    non unique email/username is provided.
    """
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="username/email not unique",
    )


def old_pass_not_matched() -> HTTPException:
    """
    Custom exception that can be raised while updating user\n
    if old password didn't match current pass.
    """
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Old pass didn't matched",
    )
