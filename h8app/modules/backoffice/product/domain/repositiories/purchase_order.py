from abc import abstractmethod
from uuid import UUID

from h8 import EntityRepositoryPortBase, LabeledUuid, Page
from h8core import AllowedAttributeTypes, Attribute, Criteria, Order

from ..entities.product import Product


class ProductPort(EntityRepositoryPortBase, Product):

    @abstractmethod
    def filter(
        self,
        limit: int,
        criteria: Criteria | None = None,
        order_by: Attribute[AllowedAttributeTypes] | None = None,
        order: Order = Order.DESCENDING,
    ) -> list[Product]: ...

    @abstractmethod
    def count(self, criteria: Criteria | None = None) -> int: ...

    @abstractmethod
    def find(
        self,
        filters: Criteria | None,
        searchtext: str | None,
        order_by: Order | None,
        order: Attribute[AllowedAttributeTypes] | None,
        page_size: int,
        page: str | None,
    ) -> Page[Product]: ...

    @abstractmethod
    def get(self, record_id: UUID) -> Product | None: ...

    @abstractmethod
    def label(self, record_id: UUID) -> LabeledUuid: ...

    @abstractmethod
    def create(self, entity: Product) -> None: ...

    @abstractmethod
    def update(
        self, record_id: UUID, changes: dict[Attribute[AllowedAttributeTypes], AllowedAttributeTypes]
    ) -> None: ...

    @abstractmethod
    def delete(self, record_id: UUID) -> None: ...
