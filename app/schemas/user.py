from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Схема с базовыми полями модели Пользователя."""
    pass


class UserCreate(schemas.BaseUserCreate):
    """Схема для создания Пользователя."""
    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Схема для обновления объекта Пользователя."""
    pass
