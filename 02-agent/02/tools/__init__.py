from .apis import get_users, get_user_by_id
from .database import get_appointments


available_tools = [
    get_users,
    get_user_by_id,
    get_appointments,
]
