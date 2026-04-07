from pathlib import Path

import customtkinter as ctk
from colors.catpuccin import catppuccin
from colors.gruvbox import gruvbox
from colors.tokyonight import tokyonight
from config_pm.config_button import ButtonConfig, create_button_config
from config_pm.frame_config import BUTTON_FRAME, HEADER_FRAME, FrameConfig
from config_pm.image_config import ImageConfig, get_icon
from config_pm.label_config import LabelConfig, create_label_config
from config_pm.window_config import POWER_MENU_WINDOW, WindowConfig
from widgets.button import Button
from widgets.frame import Frame
from widgets.image import AppImage
from widgets.label import Label
from windows.base_window import BaseWindow

from constants import THEME_COLOR
from settings.path import QtilePath


class Application(ctk.CTk, BaseWindow):
    def __init__(self) -> None:
        super().__init__()
        self.qp: Path = QtilePath()
        self.config: WindowConfig = POWER_MENU_WINDOW
        self.setup_geometry(self, config=self.config)
        self.themes: dict[str, dict[str, dict[str, str]]] = {
            "catppuccin": catppuccin,
            "gruvbox": gruvbox,
            "tokyonight": tokyonight,
        }

        self.current_theme: dict[str, dict[str, str]] = self.themes[THEME_COLOR]
        self.configure(fg_color=self.current_theme["background"]["mantle"])

        self.create_frames()
        self.create_image()
        self.create_labels()
        self.create_buttons()

        self.setup_window(self, config=self.config)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)  # Заголовок
        self.grid_rowconfigure(1, weight=1)  # Кнопки

        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)

    def create_image(self) -> None:
        """Загрузка иконок"""
        lock: ImageConfig = get_icon(self.qp.get, "lock")
        reboot: ImageConfig = get_icon(self.qp.get, "restart")
        poweroff: ImageConfig = get_icon(self.qp.get, "poweroff")
        logout: ImageConfig = get_icon(self.qp.get, "logout")

        self.lock_icon: AppImage = AppImage.from_file(lock.path, lock.size)
        self.reboot_icon: AppImage = AppImage.from_file(reboot.path, reboot.size)
        self.poweroff_icon: AppImage = AppImage.from_file(poweroff.path, poweroff.size)
        self.logout_icon: AppImage = AppImage.from_file(logout.path, logout.size)

    def create_frame_from_config(self, parent, config: FrameConfig) -> Frame:
        frame: Frame = Frame(
            parent,
            fg_color=config.fg_color,
            height=config.height,
        )
        frame.grid(
            row=config.row,
            column=config.column,
            columnspan=config.columnspan,
            sticky=config.sticky,
            pady=config.pady,
        )
        return frame

    def create_frames(self) -> None:
        """Создание фреймов через фабрику"""
        self.header_frame: Frame = self.create_frame_from_config(self, HEADER_FRAME)
        self.button_frame: Frame = self.create_frame_from_config(self, BUTTON_FRAME)

    def create_labels(self) -> None:
        title_config: LabelConfig = create_label_config(
            theme=self.current_theme,
            text="Power Menu",
        )

        self.title_label: Label = self._create_label_from_config(
            self.header_frame, title_config
        )

    def _create_label_from_config(self, parent, config: LabelConfig) -> Label:
        label = Label(
            parent,
            text=config.text,
            font=config.font,
            text_color=config.text_color,
        )
        label.pack(expand=True, fill="both")
        return label

    def create_buttons(self) -> None:
        lock_config: ButtonConfig = create_button_config(
            theme=self.current_theme,
            text="Lock",
            command=self.on_lock_click,
            bind_key="<l>",
            image=self.lock_icon,
            column=0,
            border_color=self.current_theme["accent"]["mauve"],
        )

        reboot_config: ButtonConfig = create_button_config(
            theme=self.current_theme,
            text="Reboot",
            command=self.on_reboot_click,
            bind_key="<r>",
            image=self.reboot_icon,
            column=1,
            border_color=self.current_theme["accent"]["blue"],
        )

        poweroff_config: ButtonConfig = create_button_config(
            theme=self.current_theme,
            text="Poweroff",
            command=self.on_poweroff_click,
            bind_key="<p>",
            image=self.poweroff_icon,
            column=2,
            border_color=self.current_theme["accent"]["red"],
        )

        logout_config: ButtonConfig = create_button_config(
            theme=self.current_theme,
            text="Logout",
            command=self.on_logout_click,
            bind_key="<q>",
            image=self.logout_icon,
            column=3,
            border_color=self.current_theme["accent"]["yellow"],
        )

        # Создаём кнопки: frame + config + grid
        self.button_lock: Button = self._create_button(self.button_frame, lock_config)
        self.button_reboot: Button = self._create_button(
            self.button_frame, reboot_config
        )
        self.button_poweroff: Button = self._create_button(
            self.button_frame, poweroff_config
        )
        self.button_logout: Button = self._create_button(
            self.button_frame, logout_config
        )

    def _create_button(self, parent_frame, config: ButtonConfig) -> Button:
        """Создать кнопку из конфига с frame и grid"""
        button = Button(
            parent_frame,
            text=config.text,
            command=config.command,
            image=config.image,
            compound=config.compound,
            bind_key=config.bind_key,
            fg_color=config.fg_color,
            hover_color=config.hover_color,
            text_color=config.text_color,
            font=config.font,
            width=config.width,
            height=config.height,
            border_width=config.border_width,
            border_color=config.border_color,
            corner_radius=config.corner_radius,
        )
        button.grid(
            row=config.row,
            column=config.column,
            padx=config.padx,
            pady=config.pady,
        )
        return button

    def on_lock_click(self) -> None:
        """Обработчик нажатия на кнопку блокировки"""
        self.button_lock.lock()

    def on_reboot_click(self) -> None:
        self.button_reboot.reboot()

    def on_poweroff_click(self) -> None:
        self.button_poweroff.poweroff()

    def on_logout_click(self) -> None:
        self.button_logout.logout()
