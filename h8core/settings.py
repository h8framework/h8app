__all__ = [
    "SettingsMetaclass",
]


class SettingsMetaclass(type):
    def __init__(cls, name, bases, clsdict) -> None:
        super(SettingsMetaclass, cls).__init__(name, bases, clsdict)


class Settings(metaclass=SettingsMetaclass): ...
