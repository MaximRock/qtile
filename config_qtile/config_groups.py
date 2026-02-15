from libqtile.config import Match

DEFAULT_OVERRIDES: dict[str, dict[str, object]] = {
    "9": {"matches": [Match(wm_class="Throne")]}
}

WORK_OVERRIDES: dict[str, dict[str, object]] = {
    "1": {"matches": [Match(wm_class="wezterm")]},
    "2": {"matches": [Match(wm_class="code")]},
    "9": {"matches": [Match(wm_class="Throne")]},
}
COUNT: int = 9


def setup(count: int, overrides: dict) -> list[dict]:
    base: list[dict] = []
    for group in range(1, count + 1):
        base_group: dict = {"name": str(group)}

        if str(group) in overrides:
            final_group: dict = {**base_group, **overrides[str(group)]}
        else:
            final_group: dict = base_group

        base.append(final_group)
    return base


def default() -> list[dict]:
    return setup(count=COUNT, overrides=DEFAULT_OVERRIDES)


def work() -> list[dict]:
    return setup(count=COUNT, overrides=WORK_OVERRIDES)
