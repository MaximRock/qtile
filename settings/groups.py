"""Создание и валидация групп рабочих пространств Qtile.

Модуль принимает на вход список конфигураций групп и преобразует их
в объекты `libqtile.config.Group`.

При ошибках валидации используются исключения из `exceptions/group_exceptions.py`.
"""

import re
from logging import Logger
from typing import Any

from libqtile.config import Group

from exceptions.group_exceptions import GroupError
from settings.logger import get_logger

logger: Logger = get_logger("qtile.groups", file="logger")

NAME_RE = re.compile(r"^[a-zA-Z0-9_-]{1,10}$")


def _validate_group_config(group: Any, index: int) -> dict[str, Any]:
    """Валидирует и нормализует конфигурацию одной группы."""
    if not isinstance(group, dict):
        logger.error(
            f"groups[{index}]: ожидался словарь, получено {type(group).__name__}"
        )
        raise GroupError(
            f"Элемент groups[{index}] должен быть словарём, получено: {type(group).__name__}",  # noqa: E501
            group_name="unknown",
        )

    name = group.get("name")
    if not isinstance(name, str) or not name.strip():
        logger.error(
            f"groups[{index}]: имя группы обязательно и должно быть строкой, "
            f"получено {type(name).__name__ if name is not None else 'None'}"
        )
        raise GroupError(
            f"Группа groups[{index}]: имя обязательно и должно быть строкой",
            group_name="unknown",
        )

    name = name.strip()

    if not NAME_RE.match(name):
        logger.error(
            f"groups[{index}]: имя '{name}' содержит недопустимые символы "
            f"(допустимы a-z, A-Z, 0-9, _, -, длина 1-10)"
        )
        raise GroupError(
            f"Группа groups[{index}]: имя '{name}' содержит недопустимые символы "
            f"(допустимы a-z, A-Z, 0-9, _, -, длина 1-10)",
            group_name=name,
        )

    normalized = {"name": name}

    if "matches" in group:
        normalized["matches"] = group["matches"]

    if "layout" in group:
        layout = group["layout"]
        if layout is not None and not isinstance(layout, str):
            logger.error(
                f"Группа '{name}': поле 'layout' должно быть строкой или None, "
                f"получено {type(layout).__name__}"
            )
            raise GroupError(
                f"Группа '{name}': поле 'layout' должно быть строкой или None",
                group_name=name,
            )
        normalized["layout"] = layout

    if "exclusive" in group:
        exclusive = group["exclusive"]
        if not isinstance(exclusive, bool):
            logger.error(
                f"Группа '{name}': поле 'exclusive' должно быть булевым значением, "
                f"получено {type(exclusive).__name__}"
            )
            raise GroupError(
                f"Группа '{name}': поле 'exclusive' должно быть булевым значением",
                group_name=name,
            )
        normalized["exclusive"] = exclusive

    if "spawn" in group:
        spawn = group["spawn"]
        if spawn is not None and not isinstance(spawn, (str, list)):
            logger.error(
                f"Группа '{name}': поле 'spawn' должно быть строкой, списком или None, "
                f"получено {type(spawn).__name__}"
            )
            raise GroupError(
                f"Группа '{name}': поле 'spawn' должно быть строкой, списком или None",
                group_name=name,
            )
        normalized["spawn"] = spawn

    return normalized


def create_gpups(config_groups: list[dict]) -> list[Group]:
    """Создаёт список объектов Group из конфигураций.

    Args:
        config_groups: Список словарей с полями `name`, опционально
            `matches`, `layout`, `exclusive`, `spawn`.

    Returns:
        Список объектов `libqtile.config.Group`.

    Raises:
        GroupError: При невалидной структуре конфигурации.
    """
    if not isinstance(config_groups, list):
        logger.error(
            f"create_gpups: ожидался список групп, получено {type(config_groups).__name__}"
        )
        raise GroupError(
            f"Ожидался список групп, получено: {type(config_groups).__name__}",
            group_name="unknown",
        )

    logger.info(f"Создание групп: получено {len(config_groups)} конфигураций")

    groups: list[Group] = []
    seen_names: set[str] = set()

    for index, raw_group in enumerate(config_groups):
        group_config = _validate_group_config(raw_group, index)

        name = group_config["name"]
        if name in seen_names:
            logger.warning(f"Дубликат группы '{name}' в groups[{index}], пропущен")
            continue

        seen_names.add(name)

        try:
            group = Group(**group_config)
            groups.append(group)
            logger.debug(f"Создана группа: {name}")
        except Exception as e:
            logger.error(f"Ошибка создания группы '{name}': {e}")
            raise GroupError(
                f"Не удалось создать группу '{name}': {e}",
                group_name=name,
            ) from e

    if not groups:
        logger.error("create_gpups: не создано ни одной группы — список пуст")
        raise GroupError("Список групп пуст", group_name="unknown")

    logger.info(f"Успешно создано групп: {len(groups)}")
    return groups
