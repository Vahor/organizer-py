import dataclasses
import toml

@dataclasses.dataclass
class Shortcut:
    next: str
    prev: str
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


@dataclasses.dataclass
class Organizer:
    windows: dict[int, Window]


@dataclasses.dataclass
class Config:
    shortcut: Shortcut
    organizer: Organizer

def load_config(file_path: str = "./config.toml") -> Config:
    with open(file_path, 'r') as f:
        toml_data = toml.load(f)

        windows = {}
        for position, window in toml_data['organizer'].items():
            windows[int(position)] = Window(
                **window
            )

        # add _ to numbers
        shortcuts = {}
        for key, value in toml_data['shortcut'].items():
            if key.isnumeric():
                shortcuts[f'_{key}'] = value
            else:
                shortcuts[key] = value

        return Config(
                shortcut=Shortcut(
                    **shortcuts
                ),
                
                organizer=Organizer(
                    windows=windows
                )
            )
