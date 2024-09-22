from abc import abstractmethod
from typing import Any

from h8core import RuleBaseMetaclass


class RuleBase(metaclass=RuleBaseMetaclass):
    @abstractmethod
    def is_satisfied_by(self, input: Any) -> None: ...
