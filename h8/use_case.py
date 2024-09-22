from abc import abstractmethod
from typing import dataclass_transform

from h8core import UseCaseBaseMetaclass

from .functions.capture_execute import capture_execute
from .functions.class_init import class_init


@dataclass_transform(kw_only_default=True)
class UseCaseCreateBase(metaclass=UseCaseBaseMetaclass):
    def __init__(self, /, **kwargs) -> None:
        class_init(self, **kwargs)

    def __getattribute__(self, name):
        return capture_execute(self, name)

    def on_error(self, exc: Exception):
        raise exc

    @abstractmethod
    def execute(self) -> None: ...


class UseCaseDeleteBase(metaclass=UseCaseBaseMetaclass):
    def __init__(self, /, **kwargs) -> None:
        class_init(self, **kwargs)

    def __getattribute__(self, name):
        return capture_execute(self, name)

    def on_error(self, exc: Exception):
        raise exc

    @abstractmethod
    def execute(self) -> None: ...


class UseCaseUpdateBase(metaclass=UseCaseBaseMetaclass):
    def __init__(self, /, **kwargs) -> None:
        class_init(self, **kwargs)

    def __getattribute__(self, name):
        return capture_execute(self, name)

    def on_error(self, exc: Exception):
        raise exc

    @abstractmethod
    def execute(self) -> None: ...


class UseCaseFindBase(metaclass=UseCaseBaseMetaclass):
    def __init__(self, /, **kwargs) -> None:
        class_init(self, **kwargs)

    def __getattribute__(self, name):
        return capture_execute(self, name)

    def on_error(self, exc: Exception):
        raise exc

    @abstractmethod
    def execute(self) -> None: ...


class UseCaseDetailBase(metaclass=UseCaseBaseMetaclass):
    def __init__(self, /, **kwargs) -> None:
        class_init(self, **kwargs)

    def __getattribute__(self, name):
        return capture_execute(self, name)

    def on_error(self, exc: Exception):
        raise exc

    @abstractmethod
    def execute(self) -> None: ...
