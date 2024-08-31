from typing import get_type_hints


def class_init(self, **kwargs):
    for name, _ in get_type_hints(self.__class__).items():
        in_arguments = name in kwargs

        if not in_arguments:
            raise ValueError(f"{self.__class__.__name__} constructor key argument '{name}' is missing.")

        setattr(self, name, kwargs[name])
