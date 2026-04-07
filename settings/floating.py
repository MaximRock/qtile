"""Управление плавающими окнами и правилами их отображения.

Модуль предоставляет:
- `FloatRule` — правило сопоставления окна по `wm_class` или `title`;
- `FloatingConfig` — конфигурация плавающего layout (границы, умолчания);
- `FloatingFactory` — фабрика для создания `FloatingConfig` из JSON.

При ошибках используются исключения из `exceptions/layout_exceptions.py`.
"""

import json
from dataclasses import dataclass, field
from logging import Logger
from pathlib import Path
from typing import Any

from libqtile import layout
from libqtile.config import Match

from exceptions.layout_exceptions import (
    LayoutConfigurationError,
    LayoutError,
    LayoutNotFoundError,
)
from settings.base_factory import BaseFactory
from settings.logger import get_logger
from settings.theme_controller import ThemeController

logger: Logger = get_logger("qtile.floating", file="floating")


# -------------------------
# RULE
# -------------------------
@dataclass
class FloatRule:
    """Правило для плавающих окон.

    Правило должно содержать хотя бы одно из полей:
    - `wm_class` — класс окна (например, `wezterm`, `code`);
    - `title` — заголовок окна.
    """

    wm_class: str | None = None
    title: str | None = None

    def __post_init__(self) -> None:
        if not self.wm_class and not self.title:
            logger.error(
                f"FloatRule: не указаны wm_class и title. "
                f"wm_class={self.wm_class}, title={self.title}"
            )
            raise LayoutConfigurationError(
                layout_name="FloatRule",
                parameter="wm_class|title",
                reason="Должно быть указано хотя бы одно из полей",
            )

    def to_match(self) -> Match:
        """Преобразует правило в объект Match для Qtile."""
        if self.wm_class:
            return Match(wm_class=self.wm_class)
        if self.title:
            return Match(title=self.title)

        raise LayoutError(
            "Не удалось создать Match: ни wm_class, ни title не заданы",
            layout_name="FloatRule",
        )


# -------------------------
# CONFIG
# -------------------------
@dataclass
class FloatingConfig:
    """Конфигурация плавающего layout.

    Fields:
        float_rules: Список правил для автоматического открытия окон в плавающем режиме.
        default_float_rules: Использовать стандартные правила Qtile.
        border_width: Толщина границы плавающих окон.
        border_focus: Цвет границы активного окна (hex).
        border_normal: Цвет границы неактивных окон (hex).
    """

    float_rules: list[FloatRule] = field(default_factory=list)
    default_float_rules: bool = True

    border_width: int = 1
    border_focus: str = "#ffffff"
    border_normal: str = "#000000"

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        """Валидирует поля конфигурации."""
        if not isinstance(self.float_rules, list):
            logger.error(
                f"FloatingConfig: float_rules должен быть списком, "
                f"получено: {type(self.float_rules).__name__}"
            )
            raise LayoutConfigurationError(
                layout_name="FloatingConfig",
                parameter="float_rules",
                reason="Ожидался список",
            )

        if not isinstance(self.default_float_rules, bool):
            logger.error(
                f"FloatingConfig: default_float_rules должен быть булевым значением, "
                f"получено: {type(self.default_float_rules).__name__}"
            )
            raise LayoutConfigurationError(
                layout_name="FloatingConfig",
                parameter="default_float_rules",
                reason="Ожидалось булево значение",
            )

        if not isinstance(self.border_width, int) or self.border_width < 0:
            logger.error(
                f"FloatingConfig: border_width должен быть неотрицательным целым числом, "
                f"получено: {self.border_width}"
            )
            raise LayoutConfigurationError(
                layout_name="FloatingConfig",
                parameter="border_width",
                reason="Ожидалось неотрицательное целое число",
            )

        for color_field in ("border_focus", "border_normal"):
            value = getattr(self, color_field)
            if not isinstance(value, str) or not value.startswith("#"):
                logger.error(
                    f"FloatingConfig: {color_field} должен быть hex-цветом, "
                    f"получено: {value}"
                )
                raise LayoutConfigurationError(
                    layout_name="FloatingConfig",
                    parameter=color_field,
                    reason=f"Ожидался hex-цвет (строка начинающаяся с #), получено: {value}",
                )

    def get_layout(self) -> layout.Floating:
        """Создаёт и возвращает объект layout.Floating с настроенными правилами."""
        float_rules = []

        if self.default_float_rules:
            float_rules.extend(layout.Floating.default_float_rules)

        for rule in self.float_rules:
            float_rules.append(rule.to_match())

        logger.info(
            f"Создан Floating layout: {len(float_rules)} правил, "
            f"border_width={self.border_width}"
        )

        return layout.Floating(
            float_rules=float_rules,
            border_width=self.border_width,
            border_focus=self.border_focus,
            border_normal=self.border_normal,
        )


# -------------------------
# FACTORY
# -------------------------
class FloatingFactory:
    """Фабрика для создания FloatingConfig из JSON-конфигурации темы.

    Args:
        theme_controller: Экземпляр ThemeController для доступа к путям и настройкам.
    """

    def __init__(self, theme_controller: ThemeController) -> None:
        self.tc = theme_controller

    def _load_floating_json(self) -> dict:
        """Загружает и валидирует структуру floating.json."""
        path: Path = self.tc.theme_path / "floating.json"

        if not path.exists():
            logger.error(f"Файл floating.json не найден: {path}")
            raise LayoutNotFoundError(
                layout_name="floating",
                available_layouts=[path.name],
            )

        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Некорректный JSON в {path}: {e}")
            raise LayoutConfigurationError(
                layout_name="floating",
                parameter="json",
                reason=f"Ошибка разбора JSON: {e}",
            ) from e

        if not isinstance(data, dict):
            raise LayoutConfigurationError(
                layout_name="floating",
                parameter="root",
                reason="Корень JSON должен быть объектом",
            )

        logger.debug(f"Загружен floating.json: {path}")
        return data

    def _parse_float_rules(self, rules_data: Any, resolved: dict) -> list[FloatRule]:
        """Парсит правила плавающих окон с подстановкой значений."""
        if not isinstance(rules_data, list):
            raise LayoutConfigurationError(
                layout_name="floating",
                parameter="float_rules",
                reason="Ожидался список правил",
            )

        float_rules: list[FloatRule] = []
        for i, rule in enumerate(rules_data):
            if not isinstance(rule, dict):
                raise LayoutConfigurationError(
                    layout_name="floating",
                    parameter=f"float_rules[{i}]",
                    reason="Каждое правило должно быть объектом",
                )

            wm_class = rule.get("wm_class")
            title = rule.get("title")

            # Подстановка через resolved, если значения — плейсхолдеры
            if isinstance(wm_class, str) and wm_class in resolved:
                wm_class = resolved[wm_class]
            if isinstance(title, str) and title in resolved:
                title = resolved[title]

            try:
                float_rules.append(FloatRule(wm_class=wm_class, title=title))
            except LayoutConfigurationError as e:
                logger.error(f"Ошибка правила float_rules[{i}]: {e}")
                raise

        return float_rules

    def build(self) -> FloatingConfig:
        """Создаёт и возвращает FloatingConfig из загруженного JSON.

        Returns:
            Готовый объект FloatingConfig с подставленными значениями.
        """
        data = self._load_floating_json()

        floating_config = data.get("floating", {})
        if not isinstance(floating_config, dict):
            logger.error(
                f"FloatingFactory: 'floating' должен быть объектом, "
                f"получено: {type(floating_config).__name__}"
            )
            raise LayoutConfigurationError(
                layout_name="floating",
                parameter="floating",
                reason="Ожидался объект с настройками плавающих окон",
            )

        rules_data = floating_config.get("float_rules", [])

        # Подстановка через BaseFactory
        factory = BaseFactory(
            themes=[],
            classes={},
            colors=self.tc.get_theme_color(),
            settings=self.tc.get_theme_settings(),
        )

        resolved = factory._substitute(floating_config)
        logger.debug(f"[FLOATING] resolved config: {resolved}")

        float_rules = self._parse_float_rules(rules_data, resolved)

        default_float_rules = resolved.get("default_float_rules", True)
        if not isinstance(default_float_rules, bool):
            logger.error(
                f"FloatingFactory: default_float_rules должен быть булевым значением, "
                f"получено: {default_float_rules}"
            )
            raise LayoutConfigurationError(
                layout_name="floating",
                parameter="default_float_rules",
                reason="Ожидалось булево значение",
            )

        border_width = resolved.get("border_width", 1)
        if not isinstance(border_width, int) or border_width < 0:
            logger.error(
                f"FloatingFactory: border_width должен быть неотрицательным целым числом, "
                f"получено: {border_width}"
            )
            raise LayoutConfigurationError(
                layout_name="floating",
                parameter="border_width",
                reason="Ожидалось неотрицательное целое число",
            )

        border_focus = resolved.get("border_focus", "#ffffff")
        border_normal = resolved.get("border_normal", "#000000")

        for color_name, color_value in [
            ("border_focus", border_focus),
            ("border_normal", border_normal),
        ]:
            if not isinstance(color_value, str) or not color_value.startswith("#"):
                logger.error(
                    f"FloatingFactory: {color_name} должен быть hex-цветом, "
                    f"получено: {color_value}"
                )
                raise LayoutConfigurationError(
                    layout_name="floating",
                    parameter=color_name,
                    reason=f"Ожидался hex-цвет, получено: {color_value}",
                )

        logger.info(
            f"FloatingConfig создан: {len(float_rules)} правил, "
            f"border_width={border_width}"
        )

        return FloatingConfig(
            float_rules=float_rules,
            default_float_rules=default_float_rules,
            border_width=border_width,
            border_focus=border_focus,
            border_normal=border_normal,
        )
