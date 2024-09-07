from typing import dataclass_transform, get_origin, get_type_hints

from .attribute import Attribute
from .check_subclasses_from_abract_class import check_subclasses_from_abstract_class

__all__ = [
    "EntityBaseMetaclass",
]


@dataclass_transform(kw_only_default=True)
class EntityBaseMetaclass(type):
    def __init__(cls, name, bases, clsdict) -> None:
        check_subclasses_from_abstract_class(cls, name, bases)
        if bases:
            annotations = get_type_hints(cls)
            for attr, annotation in annotations.items():
                if get_origin(annotation) is not Attribute:
                    raise TypeError(
                        f"Bad attribute '{attr}' annotation of '{name}' class. "
                        "Attributes of EntityBase subclasses should be "
                        "annotated as Attribute[...] or "
                        "Annotated[Attribute[...], ...] "
                    )

        super(EntityBaseMetaclass, cls).__init__(name, bases, clsdict)
