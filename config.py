import dataclasses
import tomllib as toml

@dataclasses.dataclass
class Shortcut:
    next: str
    prev: str

@dataclasses.dataclass
class Window:
    app_name: str | None = None
    title: str | None = None


@dataclasses.dataclass
class Organizer:
    windows: dict[int, Window]


@dataclasses.dataclass
class Config:
    shortcut: Shortcut
    organizer: Organizer

def load_config(file_path: str = "./config.toml") -> Config:
    with open(file_path, 'rb') as f:
        toml_data = toml.load(f)

        windows = {}
        for position, window in toml_data['organizer'].items():
            windows[int(position)] = Window(
                **window
            )

        return Config(
                shortcut=Shortcut(
                    **toml_data['shortcut']
                ),
                
                organizer=Organizer(
                    windows=windows
                )
            )
