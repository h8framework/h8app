from uuid import UUID

from h8 import EntityBase


class PurchaseOrder(EntityBase):
    id: UUID
