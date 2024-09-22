import importlib
import inspect
import pkgutil
from types import ModuleType
from typing import Callable, TypedDict

from .component import ComponentBase
from .entity import EntityBase, EntityRepositoryPortBase
from .enum import NullableIntEnum, NullableStrEnum, ValuableIntEnum, ValuableStrEnum
from .module import ModuleBase

__all__ = [
    "H8AppBaseMetaclass",
    "H8AppBase",
]


class ComponentObjectsTypedDict(TypedDict):
    entities: list[type[EntityBase]]
    repository_ports: list[type[EntityRepositoryPortBase]]
    repository_adapters: list[type[EntityRepositoryPortBase]]
    enums: list[type[ValuableIntEnum | ValuableStrEnum | NullableIntEnum | NullableStrEnum]]


merge_dict: Callable[[ComponentObjectsTypedDict, ComponentObjectsTypedDict], ComponentObjectsTypedDict] = (
    lambda x, y: ComponentObjectsTypedDict(
        **{key: x.get(key, []) + y.get(key, []) for key in set(list(x.keys()) + list(y.keys()))}
    )
)


def __import_objects(pymodule: ModuleType) -> ComponentObjectsTypedDict:
    objects: ComponentObjectsTypedDict = ComponentObjectsTypedDict(
        entities=[],
        enums=[],
        repository_adapters=[],
        repository_ports=[],
    )

    for item in pkgutil.iter_modules(pymodule.__path__):
        submodule = importlib.import_module(f"{pymodule.__package__}.{item.name}")

        if item.ispkg:
            objects = merge_dict(objects, __import_objects(submodule))

        for _, value in inspect.getmembers(submodule):
            if not inspect.isclass(value):
                continue

            if value.__module__ != submodule.__name__:
                continue

            if EntityRepositoryPortBase in value.__bases__:
                objects["repository_ports"].append(value)
                continue

            if EntityBase in value.__bases__:
                objects["entities"].append(value)
                continue

            if issubclass(value, EntityRepositoryPortBase):
                objects["repository_adapters"].append(value)
                continue

            if any(
                base in value.__bases__
                for base in (ValuableIntEnum, ValuableStrEnum, NullableIntEnum, NullableStrEnum)
            ):
                objects["enums"].append(value)
                continue

    return objects


def __import_components(pymodule: ModuleType) -> list[type[ComponentBase]]:
    components: list[type[ComponentBase]] = []
    for item in pkgutil.iter_modules(pymodule.__path__):
        submodule = importlib.import_module(f"{pymodule.__package__}.{item.name}")
        for _, value in inspect.getmembers(submodule):
            if not inspect.isclass(value):
                continue

            if value.__module__ != submodule.__name__:
                continue

            if issubclass(value, ComponentBase) and value is not ComponentBase:
                components_objects = __import_objects(submodule)
                component = value

                component.entities = components_objects["entities"]
                component.repository_ports = components_objects["repository_ports"]
                component.enums = components_objects["enums"]
                component.repository_adapters = components_objects["repository_adapters"]

                components.append(value)

        if item.ispkg:
            components += __import_components(submodule)

    return components


def _import_modulebase(pymodule: ModuleType) -> dict[type[ModuleBase], list[type[ComponentBase]]]:
    objects: dict[type[ModuleBase], list[type[ComponentBase]]] = {}
    modulebase = None
    for item in pkgutil.iter_modules(pymodule.__path__):
        submodule = importlib.import_module(f"{pymodule.__package__}.{item.name}")
        for _, value in inspect.getmembers(submodule):
            if not inspect.isclass(value):
                continue

            if value.__module__ != submodule.__package__:
                continue

            if issubclass(value, ModuleBase) and value is not ModuleBase:
                modulebase = value
                if modulebase not in objects:
                    objects[modulebase] = []

            break

        if item.ispkg and modulebase is not None:
            components = __import_components(submodule)
            objects[modulebase] += components

    return objects


_TARGET_H8_CLASSES = (
    ComponentBase,
    EntityBase,
    EntityRepositoryPortBase,
    ValuableStrEnum,
    ValuableIntEnum,
    NullableIntEnum,
    NullableIntEnum,
    ModuleBase,
)


class H8AppBaseMetaclass(type):

    def __init__(cls, name, bases, clsdict) -> None:
        if not bases or bases[0] is not H8AppBase:
            return super(H8AppBaseMetaclass, cls).__init__(name, bases, clsdict)

        modules_folder_list: list[ModuleType] = getattr(cls, "modules")
        for modules_folder in modules_folder_list:
            modulebase_dict = _import_modulebase(modules_folder)
            for modulebase, component_list in modulebase_dict.items():
                print("- ", modulebase.__name__)
                for component in component_list:
                    print(" " * 4 + "- ", component.__name__)

                    if component.entities:
                        print(" " * 8 + "- ", "Entities:")
                    for entity in component.entities:
                        print(" " * 12 + "- ", entity.__name__)

                    if component.repository_ports:
                        print(" " * 8 + "- ", "Repository ports:")
                    for entity in component.repository_ports:
                        print(" " * 12 + "- ", entity.__name__)

                    if component.repository_adapters:
                        print(" " * 8 + "- ", "Repository adapters:")
                    for entity in component.repository_adapters:
                        print(" " * 12 + "- ", entity.__name__)

                    if component.enums:
                        print(" " * 8 + "- ", "Enums:")
                    for entity in component.enums:
                        print(" " * 12 + "- ", entity.__name__)

            # objects = _import_modules_recursiverly(modules_folder)
            # for obj in objects:
            #     if not issubclass(obj, _TARGET_H8_CLASSES) or obj in _TARGET_H8_CLASSES:
            #         continue

            #     print(obj.__name__)

            # if issubclass(obj, ModuleBase):

            # modules = [module for _, module in inspect.getmembers(modules_folder) if inspect.ismodule(module)]

        super(H8AppBaseMetaclass, cls).__init__(name, bases, clsdict)


class AppDescriptor:
    __store: dict[type[ModuleBase], list[type[ComponentBase]]] | None = None

    def __get__(self, obj, objtype=None):
        if self.__store is None:
            raise TypeError("App is not loaded yet.")
        return self.__store

    def __set__(self, obj, value: dict[type[ModuleBase], list[type[ComponentBase]]]):
        if self.__store is not None:
            raise TypeError(f"App is already loaded.")

        self.__store = value


class H8AppBase(metaclass=H8AppBaseMetaclass):
    modules: list[ModuleType]

    app = AppDescriptor()
