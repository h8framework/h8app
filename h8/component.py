from h8core import ComponentMetaclass

from .entity import EntityBase, EntityRepositoryPortBase
from .enum import NullableIntEnum, NullableStrEnum, ValuableIntEnum, ValuableStrEnum


class ComponentEntitiesDescriptor:
    __store: list[type[EntityBase]] | None = None

    def __get__(self, obj, objtype=None):
        if self.__store is None:
            raise TypeError(f"{self.__class__.__name__}@{obj.__name__} is not loaded yet.")
        return self.__store

    def __set__(self, obj, value: list[type[EntityBase]]):
        if self.__store is not None:
            raise TypeError(f"{self.__class__.__name__}@{obj.__name__} are already loaded.")

        self.__store = value


class ComponentEntityRepositoryPortsDescriptor:
    __store: list[type[EntityRepositoryPortBase]] | None = None

    def __get__(self, obj, objtype=None):
        if self.__store is None:
            raise TypeError(f"{self.__class__.__name__}@{obj.__name__} is not loaded yet.")
        return self.__store

    def __set__(self, obj, value: list[type[EntityRepositoryPortBase]]):
        if self.__store is not None:
            raise TypeError(f"{self.__class__.__name__}@{obj.__name__} are already loaded.")

        self.__store = value


class ComponentEntityRepositoryAdaptersDescriptor:
    __store: list[type[EntityRepositoryPortBase]] | None = None

    def __get__(self, obj, objtype=None):
        if self.__store is None:
            raise TypeError(f"{self.__class__.__name__}@{obj.__name__} is not loaded yet.")
        return self.__store

    def __set__(self, obj, value: list[type[EntityRepositoryPortBase]]):
        if self.__store is not None:
            raise TypeError(f"{self.__class__.__name__}@{obj.__name__} are already loaded.")

        self.__store = value


class ComponentEnumsDescriptor:
    __store: list[type[ValuableStrEnum | ValuableIntEnum | NullableIntEnum | NullableStrEnum]] | None = None

    def __get__(self, obj, objtype=None):
        if self.__store is None:
            raise TypeError(f"{self.__class__.__name__}@{obj.__name__} is not loaded yet.")
        return self.__store

    def __set__(
        self, obj, value: list[type[ValuableStrEnum | ValuableIntEnum | NullableIntEnum | NullableStrEnum]]
    ):
        if self.__store is not None:
            raise TypeError(f"{self.__class__.__name__}@{obj.__name__} are already loaded.")

        self.__store = value


class ComponentBase(metaclass=ComponentMetaclass):
    entities = ComponentEntitiesDescriptor()
    repository_ports = ComponentEntityRepositoryPortsDescriptor()
    enums = ComponentEnumsDescriptor()
    repository_adapters = ComponentEntityRepositoryAdaptersDescriptor()
