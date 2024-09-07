from enum import StrEnum

__all__ = [
    "Order",
]


class Order(StrEnum):
    ASCENDING = "asc"
    DESCENDING = "dsc"
