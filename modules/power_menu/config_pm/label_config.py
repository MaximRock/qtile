from dataclasses import dataclass


@dataclass
class LabelConfig:
    text: str = ""
    font: tuple[str, int] = ("Jetbrains Mono", 16)
    text_color: str = ""


def create_label_config(
    text: str,
    font: tuple[str, int] = ("Jetbrains Mono", 16),
    text_color: str = "",
    **kwargs,
) -> LabelConfig:
    return LabelConfig(
        text=text,
        font=font,
        text_color=text_color,
        **kwargs,
    )


TITLE_LABEL: LabelConfig = create_label_config(
    text="Power Menu",
    font=("Jetbrains Mono", 24),
)
