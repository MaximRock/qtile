from logging import Logger

from libqtile.command.client import InteractiveCommandClient
from libqtile.config import Group, Key
from libqtile.lazy import lazy

from config_qtile.key_definitions import KEYS_CONFIG, KeyBinding
from exceptions.key_exceptions import (
    KeyBindingConflictError,
    KeyBindingExecutionError,
    KeyBindingFormatError,
)
from settings.logger import get_logger

logger: Logger = get_logger("qtile.keys", file="logger")


def _combo_to_str(modifiers: list[str], key: str) -> str:
    """Формирует строковое представление комбинации клавиш для логов/ошибок."""
    if modifiers:
        return "+".join([*modifiers, key])
    return key


def _resolve_mods(modifiers: list[str], mod: str) -> list[str]:
    """Подставляет фактический mod вместо плейсхолдера 'mod'."""
    if not isinstance(mod, str) or not mod.strip():
        logger.error("Невалидный аргумент mod: модификатор должен быть непустой строкой")
        raise KeyBindingFormatError("mod", "Модификатор mod должен быть непустой строкой")

    if not isinstance(modifiers, list):
        logger.error(
            f"Невалидный список модификаторов: ожидался list[str], получено {type(modifiers)}"
        )
        raise KeyBindingFormatError(
            str(modifiers), "Список модификаторов должен иметь тип list[str]"
        )

    normalized_mod = mod.strip()
    resolved_modifiers: list[str] = []

    for value in modifiers:
        if not isinstance(value, str) or not value.strip():
            logger.error(f"Невалидный модификатор в списке: {value}")
            raise KeyBindingFormatError(
                str(modifiers), "Каждый модификатор должен быть непустой строкой"
            )
        resolved_modifiers.append(normalized_mod if value == "mod" else value.strip())

    return resolved_modifiers


def _resolve_action(binding: KeyBinding, terminal: str):
    """Преобразует команду из конфигурации в lazy-действие Qtile."""
    if not isinstance(binding.command, str) or not binding.command.strip():
        combo = _combo_to_str(binding.modifiers, binding.key)
        logger.error(f"Пустая команда в привязке: {combo}")
        raise KeyBindingFormatError(
            combo,
            "Поле command должно быть непустой строкой",
        )

    cmd = binding.command.strip()
    combo = _combo_to_str(binding.modifiers, binding.key)

    if cmd == "spawn":
        arg: str = binding.args or ""
        if arg == "{{terminal}}":
            arg = terminal

        if not isinstance(arg, str) or not arg.strip():
            logger.error(f"Пустой аргумент команды spawn для привязки: {combo}")
            raise KeyBindingExecutionError(
                key_combination=combo,
                action=cmd,
                reason="Для команды spawn требуется непустой аргумент",
            )

        return [lazy.spawn(arg.strip())]

    parts = cmd.split(".")
    if any(not part for part in parts):
        logger.error(f"Невалидный путь команды '{cmd}' для привязки: {combo}")
        raise KeyBindingFormatError(combo, f"Невалидный путь команды: '{cmd}'")

    if parts[0] == "widget":
        if len(parts) < 3:
            logger.error(
                f"Невалидный формат widget-команды '{cmd}' для привязки: {combo}"
                )
            raise KeyBindingFormatError(
                combo,
                "Для widget-команды требуется формат 'widget.<name>.<method>'",
            )
        widget_name = parts[1]
        if not widget_name:
            logger.error(f"Пустое имя виджета в команде '{cmd}' для привязки: {combo}")
            raise KeyBindingFormatError(combo, "Имя виджета не может быть пустым")

        obj: InteractiveCommandClient = lazy.widget[widget_name]
        parts = parts[2:]
    else:
        obj = lazy

    try:
        for part in parts:
            obj = getattr(obj, part)
    except AttributeError as e:
        logger.error(f"Неизвестная команда '{cmd}' для привязки {combo}: {e}")
        raise KeyBindingExecutionError(
            key_combination=combo,
            action=cmd,
            reason=f"Неизвестная команда или атрибут: {e}",
        ) from e

    try:
        return [obj()]
    except Exception as e:
        logger.error(f"Ошибка выполнения команды '{cmd}' для привязки {combo}: {e}")
        raise KeyBindingExecutionError(
            key_combination=combo,
            action=cmd,
            reason=str(e),
        ) from e


def get_keys(mod: str = "mod1", terminal: str = "wezterm") -> list[Key]:
    """Строит список горячих клавиш из `KEYS_CONFIG` с валидацией и логированием."""
    if not isinstance(mod, str) or not mod.strip():
        logger.error("Невалидный аргумент mod в get_keys")
        raise KeyBindingFormatError("mod", "Аргумент mod должен быть непустой строкой")

    if not isinstance(terminal, str) or not terminal.strip():
        logger.error("Невалидный аргумент terminal в get_keys")
        raise KeyBindingFormatError(
            "terminal", "Аргумент terminal должен быть непустой строкой"
        )

    keys: list[Key] = []
    used_combinations: dict[str, str] = {}

    for item in KEYS_CONFIG:
        if not isinstance(item, KeyBinding):
            logger.error(f"Невалидный элемент в KEYS_CONFIG: {item}")
            raise KeyBindingFormatError(
                str(item), "Элемент KEYS_CONFIG должен быть KeyBinding"
                )

        if not isinstance(item.key, str) or not item.key.strip():
            logger.error(f"Невалидное поле key в элементе KEYS_CONFIG: {item}")
            raise KeyBindingFormatError(str(item), "Поле key должно быть непустой строкой")

        resolved_mods = _resolve_mods(item.modifiers, mod)
        combo = _combo_to_str(resolved_mods, item.key.strip())

        if combo in used_combinations:
            logger.error(
                f"Конфликт комбинации {combo}: '{used_combinations[combo]}' vs '{item.command}'"
            )
            raise KeyBindingConflictError(
                key_combination=combo,
                existing_action=used_combinations[combo],
                new_action=item.command,
            )

        actions = _resolve_action(item, terminal)

        key_obj = Key(
            resolved_mods,
            item.key.strip(),
            *actions,
            desc=item.desc,
        )
        keys.append(key_obj)
        used_combinations[combo] = item.command

    logger.info(f"Горячие клавиши успешно собраны: {len(keys)}")
    return keys


def create_group_keys(mod: str, groups: list[Group]) -> list[Key]:
    """Создаёт стандартные биндинги переключения/перемещения окон по группам."""
    if not isinstance(mod, str) or not mod.strip():
        logger.error("Невалидный аргумент mod в create_group_keys")
        raise KeyBindingFormatError("mod", "Аргумент mod должен быть непустой строкой")

    if not isinstance(groups, list):
        logger.error(f"Невалидный аргумент groups: {type(groups)}")
        raise KeyBindingFormatError("groups", "Аргумент groups должен быть списком")

    keys_group: list[Key] = []

    for group in groups:
        group_name = getattr(group, "name", None)
        if not isinstance(group_name, str) or not group_name.strip():
            logger.error(f"Невалидная группа в create_group_keys: {group}")
            raise KeyBindingFormatError(str(group), "Группа должна иметь непустое поле name")

        keys_group.extend(
            [
                Key(
                    [mod],
                    group_name,
                    lazy.group[group_name].toscreen(),
                    desc=f"Переключиться на группу {group_name}",
                ),
                Key(
                    [mod, "shift"],
                    group_name,
                    lazy.window.togroup(group_name),
                    desc=f"Переместить окно в группу {group_name}",
                ),
            ]
        )

    logger.info(f"Групповые клавиши успешно собраны: {len(keys_group)}")
    return keys_group
