import customtkinter as ctk
from PIL import Image


class AppImage(ctk.CTkImage):
    def __init__(
        self,
        light_image: Image = None,
        dark_image: Image = None,
        size: tuple[int, int] | None = None,
    ) -> None:
        super().__init__(light_image, dark_image, size)

    @classmethod
    def from_file(cls, path: str, size: tuple[int, int] | None = None):
        """Создать AppImage напрямую из файла"""
        pil_image = Image.open(path)

        return cls(
            light_image=pil_image,
            dark_image=pil_image,
            size=size,
        )
