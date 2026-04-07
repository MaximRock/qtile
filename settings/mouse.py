import json
from logging import Logger
from pathlib import Path

from libqtile.command.client import InteractiveCommandClient
from libqtile.config import Click, Drag
from libqtile.lazy import lazy

from exceptions.mouse_exceptions import (
    MouseBindingError,
    MouseConfigError,
    MouseLazyError,
)
from settings.logger import get_logger
from settings.path import QtilePath

logger: Logger = get_logger("qtile.mouse", file="mouse")


def resolve_lazy(path: str):
    """Преобразует строку пути lazy-команды в вызываемый объект Qtile."""
    if not isinstance(path, str) or not path.strip():
        logger.error(f"Некорректный путь lazy-команды: {path}")
        raise MouseLazyError(
            lazy_path=str(path),
            reason="Путь lazy-команды должен быть непустой строкой"
        )

    try:
        obj: InteractiveCommandClient = lazy
        for part in path.split("."):
            if not part:
                logger.error(f"Пустой сегмент в пути lazy-команды: {path}")
                raise MouseLazyError(
                    lazy_path=path,
                    reason="Путь содержит пустой сегмент"
                )
            obj = getattr(obj, part)

        return obj()

    except MouseLazyError:
        raise
    except Exception as e:
        logger.error(f"Не удалось преобразовать путь lazy-команды '{path}': {e}")
        raise MouseLazyError(lazy_path=path, reason=str(e)) from e


def build_mouse(config: dict):
    mouse = []

    if not isinstance(config, dict):
        logger.error(f"Некорректный тип конфигурации мыши: {type(config)}")
        raise MouseConfigError(
            parameter="config",
            reason=f"Конфигурация должна быть словарём, получено: {type(config)}"
        )

    bindings = config.get("bindings", [])

    if not isinstance(bindings, list):
        logger.error(f"Поле 'bindings' должно быть списком, получено: {type(bindings)}")
        raise MouseConfigError(
            parameter="bindings",
            reason=f"Ожидался список, получено: {type(bindings)}"
        )

    if not bindings:
        logger.warning("Конфигурация мыши загружена, но биндинги не найдены.")
        return mouse

    for index, bind in enumerate(bindings):
        if not isinstance(bind, dict):
            logger.warning(f"Некорректный элемент биндинга (не dict): {bind}")
            raise MouseBindingError(
                binding=str(bind),
                reason=f"Элемент [{index}] должен быть словарём"
            )

        try:
            bind_type = bind.get("type")
            modifiers = bind.get("modifiers", [])
            button = bind.get("button")
            lazy_path = bind.get("lazy")

            if not isinstance(modifiers, list):
                logger.warning(f"Поле modifiers должно быть списком: {bind}")
                raise MouseBindingError(
                    binding=str(bind),
                    reason="Поле 'modifiers' должно быть списком"
                )

            if not bind_type or not button or not lazy_path:
                logger.warning(f"Пропущен невалидный биндинг мыши: {bind}")
                raise MouseBindingError(
                    binding=str(bind),
                    reason="Отсутствуют обязательные поля: type, button или lazy"
                )

            if bind_type not in {"drag", "click"}:
                logger.warning(f"Неизвестный тип биндинга мыши: {bind_type}")
                raise MouseBindingError(
                    binding=str(bind),
                    reason=(
                            f"Неизвестный тип биндинга: '{bind_type}'. "
                            f"Допустимы: 'drag', 'click'"
                    )
                )

            lazy_cmd = resolve_lazy(lazy_path)

            if bind_type == "drag":
                start_cmd = None
                if "start" in bind:
                    start_value = bind.get("start")
                    if start_value is not None and not isinstance(start_value, str):
                        logger.warning(f"Поле start должно быть строкой: {bind}")
                        raise MouseBindingError(
                            binding=str(bind),
                            reason="Поле 'start' должно быть строкой"
                        )
                    if isinstance(start_value, str):
                        start_cmd = resolve_lazy(start_value)

                mouse.append(
                    Drag(
                        modifiers,
                        button,
                        lazy_cmd,
                        start=start_cmd,
                    )
                )

                logger.debug(
                    f"Добавлен DRAG-биндинг: {modifiers}+{button} -> {lazy_path}"
                    )

            elif bind_type == "click":
                mouse.append(
                    Click(
                        modifiers,
                        button,
                        lazy_cmd,
                    )
                )

                logger.debug(
                    f"Добавлен CLICK-биндинг: {modifiers}+{button} -> {lazy_path}"
                )

        except MouseBindingError:
            raise
        except MouseLazyError:
            raise
        except Exception as e:
            logger.exception(f"Не удалось собрать биндинг мыши: {bind}")
            raise MouseBindingError(
                binding=str(bind),
                reason=str(e)
            ) from e

    logger.info(f"Биндингов мыши загружено: {len(mouse)}")

    return mouse


def load_mouse():
    qp = QtilePath()

    try:
        path: Path = qp.get("config_qtile/settings_json/mouse.json")

        if not isinstance(path, Path):
            logger.error(f"Некорректный путь к конфигу мыши: {path}")
            raise MouseConfigError(
                parameter="path",
                reason=f"Ожидался объект Path, получено: {type(path)}"
            )

        if not path.exists():
            logger.error(f"Файл конфигурации мыши не найден: {path}")
            raise MouseConfigError(
                parameter="file",
                reason=f"Файл не найден: {path}"
            )

        with open(path, encoding="utf-8") as f:
            config = json.load(f)

        logger.info(f"Конфигурация мыши загружена из: {path}")

        return build_mouse(config)

    except (MouseConfigError, MouseBindingError, MouseLazyError):
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка разбора JSON в конфигурации мыши: {e}")
        raise MouseConfigError(parameter="json", reason=str(e)) from e
    except Exception as e:
        logger.exception("Непредвиденная ошибка при загрузке конфигурации мыши")
        raise MouseConfigError(parameter="load", reason=str(e)) from e
