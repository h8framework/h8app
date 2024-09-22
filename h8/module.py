from typing import Any

from h8core import AdaptersSetupBase, ModuleBaseMetaclass

from .entity import EntityBase


class AdapterMapping:
    def __init__(self, entity: type[EntityBase], impl: Any) -> None:
        raise NotImplementedError("Not Implemented")


class AdaptersSetup(AdaptersSetupBase):
    def __init__(self, *args: AdapterMapping) -> None:
        raise NotImplementedError("Not Implemented")


class ModuleBase(metaclass=ModuleBaseMetaclass):
    pass
