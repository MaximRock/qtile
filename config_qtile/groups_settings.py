"""Настройки групп (рабочих пространств) для Qtile.

Модуль определяет:
- `COUNT`: общее количество групп;
- `DEFAULT_OVERRIDES`: переопределения для профиля по умолчанию;
- `WORK_OVERRIDES`: переопределения для рабочего профиля.

Каждое переопределение сопоставляет номер группы с правилами `Match`
для автоматического размещения окон определённых приложений.
"""

from libqtile.config import Match

DEFAULT_OVERRIDES: dict[str, dict[str, object]] = {
    "9": {"matches": [Match(wm_class="Throne")]}
}

WORK_OVERRIDES: dict[str, dict[str, object]] = {
    "1": {"matches": [Match(wm_class="wezterm")]},
    "2": {"matches": [Match(wm_class="code")]},
    "9": {"matches": [Match(wm_class="Throne")]},
}

COUNT: int = 9
