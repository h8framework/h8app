from abc import abstractmethod
from uuid import UUID

from h8 import EntityRepositoryPortBase, LabeledUuid, Page
from h8core import AllowedAttributeTypes, Attribute, Criteria, Order

from ..entities.purchase_order import PurchaseOrder


class PurchaseOrderPort(EntityRepositoryPortBase, PurchaseOrder):

    @abstractmethod
    def filter(
        self,
        limit: int,
        criteria: Criteria | None = None,
        order_by: Attribute[AllowedAttributeTypes] | None = None,
        order: Order = Order.DESCENDING,
    ) -> list[PurchaseOrder]: ...

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
    ) -> Page[PurchaseOrder]: ...

    @abstractmethod
    def get(self, record_id: UUID) -> PurchaseOrder | None: ...

    @abstractmethod
    def label(self, record_id: UUID) -> LabeledUuid: ...

    @abstractmethod
    def create(self, entity: PurchaseOrder) -> None: ...

    @abstractmethod
    def update(
        self, record_id: UUID, changes: dict[Attribute[AllowedAttributeTypes], AllowedAttributeTypes]
    ) -> None: ...

    @abstractmethod
    def delete(self, record_id: UUID) -> None: ...
