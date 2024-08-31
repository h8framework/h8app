from abc import abstractmethod
from typing import Any

from h8core import SpecMetaclass


class SpecBase(metaclass=SpecMetaclass):
    @abstractmethod
    def is_satisfied_by(self, input: Any) -> None: ...
