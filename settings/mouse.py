import json
from pathlib import Path

from libqtile.config import Click, Drag
from libqtile.lazy import lazy

from settings.loger import get_logger
from settings.path import QtilePath

logger = get_logger("qtile.mouse", file="mouse")


def resolve_lazy(path: str):
    """
    Превращает строку:
        "window.set_position_floating"
    в:
        lazy.window.set_position_floating()
    """
    try:
        obj = lazy
        for part in path.split("."):
            obj = getattr(obj, part)

        return obj()

    except Exception as e:
        logger.error(f"Failed to resolve lazy path '{path}': {e}")
        return None


def build_mouse(config: dict):
    mouse = []
    bindings = config.get("bindings", [])

    if not bindings:
        logger.warning("Mouse config loaded but no bindings found.")
        return mouse

    for bind in bindings:
        try:
            bind_type = bind.get("type")
            modifiers = bind.get("modifiers", [])
            button = bind.get("button")
            lazy_path = bind.get("lazy")

            if not bind_type or not button or not lazy_path:
                logger.warning(f"Invalid mouse binding skipped: {bind}")
                continue

            lazy_cmd = resolve_lazy(lazy_path)
            if lazy_cmd is None:
                continue

            if bind_type == "drag":
                start_cmd = None
                if "start" in bind:
                    start_cmd = resolve_lazy(bind["start"])

                mouse.append(
                    Drag(
                        modifiers,
                        button,
                        lazy_cmd,
                        start=start_cmd,
                    )
                )

                logger.debug(f"Added DRAG binding: {modifiers}+{button} -> {lazy_path}")

            elif bind_type == "click":
                mouse.append(
                    Click(
                        modifiers,
                        button,
                        lazy_cmd,
                    )
                )

                logger.debug(
                    f"Added CLICK binding: {modifiers}+{button} -> {lazy_path}"
                )

            else:
                logger.warning(f"Unknown mouse binding type: {bind_type}")

        except Exception:
            logger.exception(f"Failed to build mouse binding: {bind}")

    logger.info(f"Mouse bindings loaded: {len(mouse)}")

    return mouse


def load_mouse():
    qp = QtilePath()

    try:
        path: Path = qp.get("config_qtile/theme/settings_json/mouse.json")

        if not path.exists():
            logger.error(f"Mouse config file does not exist: {path}")
            return []

        with open(path, encoding="utf-8") as f:
            config = json.load(f)

        logger.info(f"Mouse config loaded from: {path}")

        return build_mouse(config)

    except json.JSONDecodeError as e:
        logger.error(f"JSON parse error in mouse config: {e}")

    except Exception:
        logger.exception("Unexpected error while loading mouse config")

    return []





# def get_mouse(mod: str) -> list[Click | Drag]:
#    return [
#        Drag(
#            [mod],
#            "Button1",
#            lazy.window.set_position_floating(),
#            start=lazy.window.get_position(),
#        ),
#        Drag(
#            [mod],
#            "Button3",
#            lazy.window.set_size_floating(),
#            start=lazy.window.get_size(),
#        ),
#        Click([mod], "Button2", lazy.window.bring_to_front()),
#    ]
