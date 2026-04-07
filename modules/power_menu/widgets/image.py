from pathlib import Path

import customtkinter as ctk
from config_pm.exceptions import ImageWidgetsError
from PIL import Image


class AppImage(ctk.CTkImage):
    """
    Обёртка над CTkImage с валидацией и удобным созданием из файла.

    Аргументы:
        light_image (PIL.Image.Image | None): изображение для светлой темы
        dark_image (PIL.Image.Image | None): изображение для тёмной темы
        size (tuple[int, int] | None): размер (width, height)
    """

    def __init__(
        self,
        light_image: Image.Image | None = None,
        dark_image: Image.Image | None = None,
        size: tuple[int, int] | None = None,
    ) -> None:
        """Инициализация изображения с проверками."""

        # Проверка изображений
        if light_image is None and dark_image is None:
            raise ImageWidgetsError("AppImage: нужно передать хотя бы одно изображение")

        if light_image is not None and not isinstance(light_image, Image.Image):
            raise ImageWidgetsError(
                f"AppImage: light_image должен быть PIL.Image.Image, получено {type(light_image).__name__}"  # noqa: E501
            )

        if dark_image is not None and not isinstance(dark_image, Image.Image):
            raise ImageWidgetsError(
                f"AppImage: dark_image должен быть PIL.Image.Image, получено {type(dark_image).__name__}"  # noqa: E501
            )

        # Проверка size
        if size is not None:
            if (
                not isinstance(size, tuple)
                or len(size) != 2
                or not all(isinstance(i, int) for i in size)
            ):
                raise ImageWidgetsError(
                    "AppImage: size должен быть tuple[int, int], например (32, 32)"
                )

            if size[0] <= 0 or size[1] <= 0:
                raise ImageWidgetsError("AppImage: размер должен быть положительным")

        super().__init__(light_image, dark_image, size)

    @classmethod
    def from_file(cls, path: str | Path, size: tuple[int, int] | None = None):
        """
        Создать AppImage из файла.

        Аргументы:
            path (str | Path): путь до изображения
            size (tuple[int, int] | None): размер (width, height)

        Исключения:
            FileNotFoundError: если файл не найден
            ValueError: если путь не является файлом
            OSError: если файл не является изображением
        """

        if not isinstance(path, (str, Path)):
            raise ImageWidgetsError(
                f"AppImage.from_file: path должен быть str или Path, получено {
                    type(path).__name__
                }"
            )

        path = Path(path)

        if not path.exists():
            raise ImageWidgetsError(f"AppImage: файл не найден -> {path}")

        if not path.is_file():
            raise ImageWidgetsError(f"AppImage: это не файл -> {path}")

        try:
            pil_image: Image.Image = Image.open(path).convert("RGBA")
        except Exception as e:
            raise ImageWidgetsError(
                f"AppImage: ошибка загрузки изображения: {e}"
            ) from e

        return cls(
            light_image=pil_image,
            dark_image=pil_image,
            size=size,
        )
