from dataclasses import dataclass

from .exceptions import ConfigError, LabelConfigError, ThemeError


@dataclass(slots=True)
class LabelConfig:
    """
    Конфигурация текстового элемента (Label) для UI.

    Атрибуты:
        text (str):
            Текст, отображаемый в label.

        font (tuple[str, int]):
            Шрифт в формате (имя, размер).

        text_color (str | None):
            Цвет текста. Если None — берётся из theme.
    """
    text: str
    font: tuple[str, int]
    text_color: str | None = None


def create_label_config(
    theme: dict,
    text: str = "Power Menu",
    text_color: str | None = None,
    font: tuple[str, int] = ("Jetbrains Mono", 24),
) -> LabelConfig:
    """
    Фабрика для создания конфигурации label с валидацией и поддержкой темы.

    Если text_color не задан, автоматически используется:
        theme["text"]["primary"]

    Args:
        theme (dict):
            Словарь темы.

        text (str, optional):
            Текст label. По умолчанию "Power Menu".

        text_color (str | None, optional):
            Цвет текста. Если None — берётся из theme.

        font (tuple[str, int], optional):
            Шрифт в формате (имя, размер).
            По умолчанию ("Jetbrains Mono", 24).
    Raises:
        ThemeError:
            Если theme некорректен или отсутствует ключ ["text"]["primary"].

        LabelConfigError:
            Если text или font имеют неверный формат.

        ConfigError:
            Если произошла ошибка при создании конфигурации.

    Returns:
        LabelConfig:
            Готовый объект конфигурации label.

    Пример:
        >>> config = create_label_config(
        ...     theme=theme,
        ...     text="Power Menu"
        ... )
    """

    if not isinstance(theme, dict) or not theme:
        raise ThemeError("theme должен быть непустым словарём")

    if not text:
        raise LabelConfigError("text обязателен")

    if not (
        isinstance(font, tuple)
        and len(font) == 2
        and isinstance(font[0], str)
        and isinstance(font[1], int)
    ):
        raise LabelConfigError("font должен быть tuple[str, int]")

    if text_color is None:
        try:
            text_color = theme["text"]["primary"]
        except KeyError as e:
            raise ThemeError("Не найден ключ 'text.primary' в теме") from e

    try:
        return LabelConfig(
            text=text,
            font=font,
            text_color=text_color,
        )
    except Exception as e:
        raise ConfigError("Ошибка конфигурации label") from e
