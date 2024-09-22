from uuid import UUID

from h8 import Attribute, EntityBase

from ..enums.status import PurchaseOrderStatusEnum


class PurchaseOrder(EntityBase):
    id: Attribute[UUID]
    customer_id: Attribute[UUID]
    status: Attribute[PurchaseOrderStatusEnum]
