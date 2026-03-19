#!/usr/bin/env nix-shell
#! nix-shell -i python3 ../../shell.nix

import customtkinter as tk
import subprocess

from pathlib import Path

from PIL import Image
from settings.path import QtilePath
from color import mocha


qp: QtilePath = QtilePath()

def reboot():
    subprocess.run(["systemctl", "reboot"])
    app.destroy()


def lock():
    subprocess.run(["xlock"])
    app.destroy()


app = tk.CTk()
app.geometry("600x250")
app.resizable(False, False)

app.configure(fg_color="#181825")

current_dir: Path = qp.get("modules/power_menu/icons/restart.png")
lock_file: Path = qp.get("modules/power_menu/icons/lock.png")

reboot_icon = tk.CTkImage(
    dark_image=Image.open(current_dir),
    size=(40, 40),
)

lock_icon = tk.CTkImage(
    dark_image=Image.open(lock_file),
    size=(40, 40),
)

# Фрейм для заголовка
header_frame = tk.CTkFrame(app, fg_color="transparent", height=60)
header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(10, 0))
header_frame.grid_propagate(False)  # Запрещаем изменение размера

# Заголовок внутри фрейма
title_label = tk.CTkLabel(
    header_frame,
    text="Power Menu",
    font=("Jetbrains Mono", 24),
    text_color=mocha["text"],
)
title_label.pack(expand=True, fill="both")

# Фрейм для кнопок
buttons_frame = tk.CTkFrame(app, fg_color="transparent")
buttons_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)

# Кнопки внутри фрейма
btn_reboot = tk.CTkButton(
    buttons_frame,
    text="Reboot",
    command=reboot,
    image=reboot_icon,
    compound="top",
    fg_color=mocha["surface0"],
    hover_color=mocha["surface1"],
    text_color=mocha["text"],
    font=("Jetbrains Mono", 24),
    corner_radius=3,
    width=150,
    height=160,
    border_width=2,
    border_color=mocha["mauve"],
)
btn_reboot.grid(row=0, column=0, padx=(30, 10), pady=5)

btn_lock = tk.CTkButton(
    buttons_frame,
    text="Lock",
    command=lock,
    image=lock_icon,
    compound="top",
    fg_color=mocha["surface0"],
    hover_color=mocha["surface1"],
    text_color=mocha["text"],
    font=("Jetbrains Mono", 24),
    corner_radius=3,
    width=150,
    height=160,
    border_width=2,
    border_color=mocha["blue"],
)
btn_lock.grid(row=0, column=1, padx=(10, 30), pady=10)

# Настройка сетки
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=0)  # Заголовок
app.grid_rowconfigure(1, weight=1)  # Кнопки

buttons_frame.grid_columnconfigure(0, weight=1)
buttons_frame.grid_columnconfigure(1, weight=1)

app.mainloop()

