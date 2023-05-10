from fastapi import Depends, Request, status

from src.dependencies import get_current_user, redis_conn
from src.endpoints.auth.auth_utils import get_jwt_exp
from src.endpoints.auth.router_init import router


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    request: Request, user: dict = Depends(get_current_user)
) -> dict[str, str]:
    """
    Logs out the authenticated user by storing the token in the redis blacklist
    """
    token = request.headers.get("authorization").split()[1]
    redis_conn.setex(f"bl_{token}", get_jwt_exp(token), token)
    return {"status": "success", "message": "user logged out"}
