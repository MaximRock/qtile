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
