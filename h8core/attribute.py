# pyright: reportAttributeAccessIssue=false, reportIncompatibleMethodOverride=false
from datetime import date, datetime
from enum import Enum
from typing import Any, Generic, Type, TypeAlias, TypeVar, TypeVarTuple, Union, overload
from uuid import UUID

from .criteria import (
    EqCriteria,
    GeCriteria,
    GtCriteria,
    InCriteria,
    LeCriteria,
    LikeCriteria,
    LtCriteria,
    NeCriteria,
    NotLikeCriteria,
)

__all__ = [
    "AllowedAttributeTypes",
    "Attribute",
]

AllowedAttributeTypes: TypeAlias = Union[str, bool, int, float, UUID, date, datetime, Enum, None]

_T = TypeVar("_T", bound=AllowedAttributeTypes)
_T_tuple = TypeVarTuple("_T_tuple")


class Attribute(Generic[_T, *_T_tuple]):
    parent_class: Type[Any]
    type: tuple[Type]
    name: str
    private_name: str
    value: "Attribute[_T, *_T_tuple]" | _T
    constraints: tuple[Any]

    def __init__(self, _cls, _field, _type, _value, _constraints) -> None:
        self.parent_class = _cls
        self.name = _field
        self.private_name = "__" + _field
        self.type = _type
        self.value = _value
        self.constraints = _constraints

    def __set_name__(self, owner, name):
        self.name = name
        self.private_name = "__" + name

    @overload
    def __get__(self, obj: None, objcls) -> "Attribute[_T, *_T_tuple]": ...

    @overload
    def __get__(self, obj, objcls) -> _T: ...

    def __get__(self, obj, objcls):
        if obj is None:
            return self

        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        setattr(obj, self.private_name, value)

    def __hash__(self) -> int:
        return hash((self.parent_class, self.name))

    def __repr__(self) -> str:
        return f"{self.parent_class.__name__}.{self.name}[{self.type[0].__name__}]"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return EqCriteria(self, other)

    def __ne__(self, other):
        return NeCriteria(self, other)

    def __lt__(self, other):
        return LtCriteria(self, other)

    def __le__(self, other):
        return LeCriteria(self, other)

    def __gt__(self, other):
        return GtCriteria(self, other)

    def __ge__(self, other):
        return GeCriteria(self, other)

    def __contains__(self, other):
        return InCriteria(self, other)

    def like(self, other):
        return LikeCriteria(self, other)

    def not_like(self, other):
        return NotLikeCriteria(self, other)
