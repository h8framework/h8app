from typing import Any, get_type_hints

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
    ) -> "list[EntityBase]": ...

    def find(
        self,
        filters: Filter | None,
        searchtext: str | None,
        order_by: OrderByStrEnum | None,
        order: CoreOrderStrEnum | None,
        page_size: int,
        page: str | None,
    ) -> IPage[Entity]: ...

    def get(self, record_id: UUID) -> Entity | None: ...

    def label(self, record_id: UUID) -> LabeledIdModel: ...

    def create(self, entity: Entity) -> None: ...

    def update(self, record_id: UUID, changes: dict[str, Any]) -> None: ...

    def delete(self, record_id: UUID) -> None: ...
