from typing import TypedDict


class Page[T](TypedDict):
    next: str | None
    previous: str | None
    page_size: int
    total: int
    records: list[T]
