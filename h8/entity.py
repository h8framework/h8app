from typing import Any, Self, get_type_hints
from uuid import UUID

from h8core import AllowedAttributeTypes, Attribute, Criteria, EntityBaseMetaclass, Order


class EntityBase(metaclass=EntityBaseMetaclass):
    def __init__(self, /, **kwargs: Any) -> None:
        for name, _ in get_type_hints(self).items():  # pylint: disable=no-member
            in_arguments = name in kwargs

            if not in_arguments:
                raise ValueError(f"{self.__class__.__name__} constructor key argument '{name}' is missing.")

            else:
                setattr(self, name, kwargs[name])

    def filter(
        self,
        limit: int,
        criteria: Criteria | None = None,
        order_by: Attribute[AllowedAttributeTypes] | None = None,
        order: Order = Order.DESCENDING,
    ) -> list[Self]: ...

    def find(
        self,
        filters: Criteria | None,
        searchtext: str | None,
        order_by: Order | None,
        order: Attribute[AllowedAttributeTypes] | None,
        page_size: int,
        page: str | None,
    ) -> IPage[Self]: ...

    def get(self, record_id: UUID) -> Self | None: ...

    def label(self, record_id: UUID) -> LabeledIdModel: ...

    def create(self, entity: Self) -> None: ...

    def update(self, record_id: UUID, changes: dict[str, Any]) -> None: ...

    def delete(self, record_id: UUID) -> None: ...
