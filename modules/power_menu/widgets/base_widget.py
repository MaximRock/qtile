from config_pm.exceptions import WidgetsError


class BaseWidget:
    """Базовый класс с chainable API и базовыми проверками."""

    def grid(self, **kwargs):

        if hasattr(self, "pack_kwargs"):
            raise WidgetsError("Нельзя использовать одновременно pack и grid")

        if not isinstance(kwargs, dict):
            raise WidgetsError("grid: kwargs должен быть dict")

        self.grid_kwargs = kwargs
        super().grid(**kwargs)
        return self

    def pack(self, **kwargs):

        if hasattr(self, "grid_kwargs"):
            raise WidgetsError("Нельзя использовать одновременно grid и pack")

        if not isinstance(kwargs, dict):
            raise WidgetsError("pack: kwargs должен быть dict")

        self.pack_kwargs = kwargs
        super().pack(**kwargs)
        return self

    def configure(self, **kwargs):

        if not isinstance(kwargs, dict):
            raise WidgetsError("configure: kwargs должен быть dict")

        super().configure(**kwargs)
        return self
