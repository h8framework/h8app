from types import ModuleType
from typing import Any

from h8core import MiddlewareBase, ModuleMetaclass

from .entity import EntityBase


class AdapterMapping:
    def __init__(self, entity: type[EntityBase], impl: Any) -> None:
        raise NotImplementedError("Not Implemented")


class Adapters:
    def __init__(self, *args: AdapterMapping) -> None:
        raise NotImplementedError("Not Implemented")


class Components:
    def __init__(self, *args: ModuleType) -> None:
        raise NotImplementedError("Not Implemented")


class Middlewares:
    def __init__(self, *args: MiddlewareBase) -> None:
        raise NotImplementedError("Not Implemented")


class ModuleBase(metaclass=ModuleMetaclass):
    pass
