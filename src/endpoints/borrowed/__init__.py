from src.endpoints.borrowed.delete import delete_by_id
from src.endpoints.borrowed.get import (
    get_all_borrowed,
    get_all_borrowed_for_any_user,
    get_all_borrowed_for_logged_in_user,
    get_borrowed_by_id,
)
from src.endpoints.borrowed.post import create_borrowed
from src.endpoints.borrowed.put import (
    return_borrowed_for_any_user,
    return_borrowed_for_user,
    update_borrowed_by_id,
)
from src.endpoints.borrowed.router_init import router
