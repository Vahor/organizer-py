import dataclasses
import toml


@dataclasses.dataclass
class Shortcut:
    next: str
    prev: str
    quit: str
    _1: str
    _2: str
    _3: str
    _4: str
    _5: str
    _6: str
    _7: str
    _8: str
    _9: str

    def __getitem__(self, item):
        return getattr(self, item)


@dataclasses.dataclass
class Window:
    app_name: str | None = None
    title: str | None = None

    def name(self):
        if self.app_name and self.title:
            return f"{self.app_name} - {self.title}"
        elif self.app_name:
            return self.app_name
        elif self.title:
            return self.title


@dataclasses.dataclass
class Organizer:
    windows: dict[int, Window]


@dataclasses.dataclass
class Config:
    shortcut: Shortcut
    organizer: Organizer


def load_config(file_path: str = "./config.toml") -> Config:
    with open(file_path, "r") as f:
        toml_data = toml.load(f)

        windows = {}
        max_position = 9
        for i in range(max_position):
            data = toml_data["organizer"].get(str(i))
            windows[i] = Window(**data) if data else None

        # add _ to numbers
        shortcuts = {}
        for key, value in toml_data["shortcut"].items():
            if key.isnumeric():
                shortcuts[f"_{key}"] = value
            else:
                shortcuts[key] = value

        return Config(
            shortcut=Shortcut(**shortcuts), organizer=Organizer(windows=windows)
        )
