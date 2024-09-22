from uuid import UUID

from h8 import Attribute, EntityBase


class Product(EntityBase):
    id: Attribute[UUID]
    name: Attribute[str]
    price: Attribute[int]
    stock: Attribute[int]
