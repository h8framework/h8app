from uuid import UUID

from h8 import AdapterChoiceBase, LabeledUuid, Page
from h8app.settings.enviroment import EnvironmentSettings
from h8core import AllowedAttributeTypes, Attribute, Criteria, Order

from ...domain.entities.purchase_order import PurchaseOrder
from ...domain.repositiories.purchase_order import PurchaseOrderPort


class AdapterChoice(AdapterChoiceBase):
    settings = EnvironmentSettings()

    def __call__(self) -> bool:
        return self.settings.ENVIRONMENT_DEVMODE is True


class PurchaseOrderAdapter(PurchaseOrderPort, AdapterChoice):

    def filter(
        self,
        limit: int,
        criteria: Criteria | None = None,
        order_by: Attribute[AllowedAttributeTypes] | None = None,
        order: Order = Order.DESCENDING,
    ) -> list[PurchaseOrder]: ...

    def count(self, criteria: Criteria | None = None) -> int: ...

    def find(
        self,
        filters: Criteria | None,
        searchtext: str | None,
        order_by: Order | None,
        order: Attribute[AllowedAttributeTypes] | None,
        page_size: int,
        page: str | None,
    ) -> Page[PurchaseOrder]: ...

    def get(self, record_id: UUID) -> PurchaseOrder | None: ...

    def label(self, record_id: UUID) -> LabeledUuid: ...

    def create(self, entity: PurchaseOrder) -> None: ...

    def update(
        self, record_id: UUID, changes: dict[Attribute[AllowedAttributeTypes], AllowedAttributeTypes]
    ) -> None: ...

    def delete(self, record_id: UUID) -> None: ...
