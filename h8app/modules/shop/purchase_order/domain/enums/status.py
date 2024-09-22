from h8 import ValuableStrEnum


class PurchaseOrderStatusEnum(ValuableStrEnum):
    PROCESSING = "processing"
    PENDING_SHIPMENT = "pending_shipment"
    SENT = "sent"
