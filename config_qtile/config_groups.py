"""Конфигурация групп (рабочих пространств) для Qtile.

Модуль отвечает за:
- `GroupConfig`: датакласс для представления одной группы;
- `setup(...)`: фабричную функцию создания списка групп с учётом переопределений;
- `default()` / `work()`: готовые наборы групп для разных профилей.

Группы создаются на основе `COUNT` и соответствующих `OVERRIDES` из `groups_settings.py`.
"""

from dataclasses import dataclass, field

from libqtile.config import Match

from config_qtile.groups_settings import COUNT, DEFAULT_OVERRIDES, WORK_OVERRIDES


@dataclass
class GroupConfig:
    """Конфигурация одной группы (рабочего пространства) в Qtile.

    Attrs:
        name: Имя группы (обычно цифра `"1"`...`"9"`).
        matches: Список условий `Match` для автоматического размещения окон.
        layout: Название раскладки для этой группы (опционально).
        exclusive: Эксклюзивный режим — окна не могут делить пространство с другими.
        spawn: Команда(ы) для автоматического запуска при создании группы.
    """

    name: str
    matches: list[Match] = field(default_factory=list)
    layout: str | None = None
    exclusive: bool = False
    spawn: str | list[str] | None = None


def setup(count: int, overrides: dict) -> list[dict]:
    """Создаёт список групп с учётом переопределений.

    Args:
        count: Количество групп для создания.
    overrides: Словарь переопределений в формате `{номер_группы: {поля}}`.

    Returns:
        Список словарей с конфигурацией каждой группы.
    """
    base: list[dict] = []
    for group in range(1, count + 1):
        base_group: dict = {"name": str(group)}

        if str(group) in overrides:
            final_group: dict = {**base_group, **overrides[str(group)]}
        else:
            final_group: dict = base_group

        base.append(final_group)
    return base


def default() -> list[dict]:
    """Возвращает конфигурацию групп по умолчанию.

    Использует `DEFAULT_OVERRIDES` из `groups_settings.py`.
    """
    return setup(count=COUNT, overrides=DEFAULT_OVERRIDES)


def work() -> list[dict]:
    """Возвращает конфигурацию групп для рабочего профиля.

    Использует `WORK_OVERRIDES` из `groups_settings.py`.
    """
    return setup(count=COUNT, overrides=WORK_OVERRIDES)