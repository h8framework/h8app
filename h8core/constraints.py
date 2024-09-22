from dataclasses import dataclass
from typing import get_type_hints

from .attribute import Attribute
from .bases import ContraintsBase
from .entity_port import EntityBaseMetaclass

__all__ = [
    "StringConstraints",
]


def get_searcheable_attributes(entity: type[EntityBaseMetaclass]) -> tuple[Attribute[str], ...]:
    attributes = get_type_hints(entity)
    searcheable_attrs: list[Attribute[str]] = []
    for attr_name, annotation in attributes.items():
        if annotation is not Attribute[str]:
            continue

        attr: Attribute[str] = getattr(entity, attr_name)
        for constraint in attr.constraints:
            if not isinstance(constraint, StringConstraints):
                continue

            if constraint.searcheable:
                searcheable_attrs.append(attr)

    return tuple(searcheable_attrs)


@dataclass
class StringConstraints(ContraintsBase):
    searcheable: bool | None = None
