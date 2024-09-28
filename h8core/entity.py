import inspect
from typing import dataclass_transform, get_origin, get_type_hints

from .adapter import AdapterChoiceBase
from .attribute import Attribute
from .check_subclasses_from_abract_class import check_subclasses_from_abstract_class

__all__ = [
    "EntityBaseMetaclass",
]

_PORTS = {}
_ENTITIES = {}
_ADAPTERS = {}


@dataclass_transform(kw_only_default=True)
class EntityBaseMetaclass(type):
    def __init__(cls, name, bases, clsdict) -> None:
        check_subclasses_from_abstract_class(cls, name, bases, 2)

        if bases and "EntityBase" in bases[0].__name__:
            annotations = get_type_hints(cls)
            for attr, annotation in annotations.items():
                if get_origin(annotation) is not Attribute:
                    raise TypeError(
                        f"Bad attribute '{attr}' annotation of '{name}' class. "
                        "Attributes of EntityBase subclasses should be "
                        "annotated as Attribute[...] or "
                        "Annotated[Attribute[...], ...] "
                    )

        if bases and "EntityRepositoryPortBase" in bases[0].__name__:
            entity = bases[1]
            if entity in _ENTITIES:
                raise TypeError(
                    f"Entity '{entity.__name__}' is already mapped to port "
                    f"'{_ENTITIES[entity].__name__}' and cannot be re-mapped to '{cls.__name__}'."
                    "Please make sure that the port is not declared twice for the same entity."
                )

            _PORTS[cls] = entity
            _ENTITIES[entity] = cls

            # It can handle relationship between Entities and their Ports

        if bases and bases[0] in _PORTS:
            port = bases[0]
            chosen = True
            if len(bases) > 1:
                adapter_choice = bases[1]
                if inspect.isclass(adapter_choice) and issubclass(adapter_choice, AdapterChoiceBase):
                    adapter_choice_instance = adapter_choice()
                    chosen = adapter_choice_instance()

                if not inspect.isclass(adapter_choice) and isinstance(adapter_choice, AdapterChoiceBase):
                    chosen = adapter_choice()

            if chosen and port in _ADAPTERS:
                raise TypeError(
                    f"Port '{port.__name__}' is already mapped to adapter "
                    f"'{_ADAPTERS[port].__name__}' and cannot be re-mapped to '{cls.__name__}'."
                    "Please make sure that AdapterChoiceBase is correctly configured."
                )

            if chosen:
                _ADAPTERS[port] = cls

            # It can handle relationship between Ports and their Adapters

        super(EntityBaseMetaclass, cls).__init__(name, bases, clsdict)
