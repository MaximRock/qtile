from dataclasses import dataclass


@dataclass
class Theme:
    name: str
    config: dict = None

    def __post_init__(self) -> None:
        if self.config is None:
            self.config = {}
