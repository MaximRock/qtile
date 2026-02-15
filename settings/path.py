
from pathlib import Path


class QtilePath:
    def __init__(self, base_path: str | None = None) -> None:
        """Простой класс для работы с путями в Qtile."""
        if base_path is None:
            self.base: Path = Path.home() / ".config" / "qtile"
        else:
            self.base: Path = Path(base_path).expanduser()

    def get(self, subpath: str | Path | None) -> Path:
        """
        Получить путь относительно base.
        Args:
            subpath: Подпуть. Если None, возвращается base.
        Returns:
            Path объект
        """
        if subpath is None:
            return self.base
        return self.base / subpath

    def ensure(self, subpath: str | None = None) -> Path:
        """
        Получить путь и создать директорию, если не существует.
        Args:
            subpath: Подпуть. Если None, используется base.
        Returns:
            Path объект (директория создана)
        """
        path = self.get(subpath)
        path.mkdir(parents=True, exist_ok=True)
        return path
