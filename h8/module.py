from types import ModuleType
from typing import Any

from h8core import (
    AdaptersSetupBase,
    ComponentsSetupBase,
    MiddlewareBase,
    MiddlewaresSetupBase,
    ModuleMetaclass,
)

from .entity import EntityBase


class AdapterMapping:
    def __init__(self, entity: type[EntityBase], impl: Any) -> None:
        raise NotImplementedError("Not Implemented")


class AdaptersSetup(AdaptersSetupBase):
    def __init__(self, *args: AdapterMapping) -> None:
        raise NotImplementedError("Not Implemented")


class ComponentsSetup(ComponentsSetupBase):
    def __init__(self, *args: ModuleType) -> None:
        raise NotImplementedError("Not Implemented")


class MiddlewaresSetup(MiddlewaresSetupBase):
    def __init__(self, *args: MiddlewareBase) -> None:
        raise NotImplementedError("Not Implemented")


class ModuleBase(metaclass=ModuleMetaclass):
    pass
