class PowerMenuError(Exception):
    """Базовое исключение"""

    pass


class ConfigError(PowerMenuError):
    """Ошибка конфигурации"""

    pass


class ThemeError(ConfigError):
    """Ошибка цветовой темы"""

    pass


class ButtonConfigError(ConfigError):
    """Ошибка в конфигурации кнопки"""

    pass


class FrameConfigError(ConfigError):
    """Ошибка в конфигурации frame"""

    pass


class LabelConfigError(ConfigError):
    """Ошибка в конфигурации label"""

    pass


class ImageConfigError(ConfigError):
    """ошибка в конфигурации image"""

    pass


class WindowConfigError(ConfigError):
    """Ошибка в конфигурации window"""

    pass


class WidgetsError(PowerMenuError):
    """Ошибки в конфигурации widgets"""

    pass


class ButtonWidgetsError(WidgetsError):
    """Ошибка в конфигурации button widget"""

    pass


class LabelWidgetsError(WidgetsError):
    """Ошибка в конфигурации label widget"""

    pass


class ImageWidgetsError(WidgetsError):
    """Ошибка в конфигурации image widget"""

    pass


class FrameWidgetsError(WidgetsError):
    """Ошибка в конфигурации frame widget"""

    pass
