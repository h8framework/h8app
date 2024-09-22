from typing import TypedDict
from uuid import UUID


class LabeledUuid(TypedDict):
    label: str
    value: UUID


class LabeledStr(TypedDict):
    label: str
    value: str


class LabeledInt(TypedDict):
    label: str
    value: int


class LabeledNone(TypedDict):
    label: str
    value: None
