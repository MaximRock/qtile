"""Исключения, связанные с группами рабочих пространств."""

from exceptions.base_exceptions import QtileConfigError


class GroupError(QtileConfigError):
    """Базовое исключение для ошибок групп."""

    def __init__(self, message: str, group_name: str | None = None) -> None:
        self.group_name: str | None = group_name
        super().__init__(message, component="Group")


class GroupNotFoundError(GroupError):
    """Группа не найдена."""

    def __init__(self, group_name: str, available_groups: list[str] | None = None) -> None:
        self.group_name = group_name
        self.available_groups: list[str] = available_groups or []
        message = f"Группа '{group_name}' не найдена"
        if self.available_groups:
            message += f". Доступные группы: {', '.join(self.available_groups)}"
        super().__init__(message, group_name)


class GroupAlreadyExistsError(GroupError):
    """Группа уже существует."""

    def __init__(self, group_name: str) -> None:
        self.group_name = group_name
        super().__init__(f"Группа '{group_name}' уже существует", group_name)


class GroupMatchError(GroupError):
    """Ошибка сопоставления приложения с группой."""

    def __init__(self, wm_class: str, group_name: str) -> None:
        self.wm_class: str = wm_class
        self.group_name = group_name
        super().__init__(
            f"Не удалось сопоставить приложение '{wm_class}' с группой '{group_name}'",
            group_name
        )
