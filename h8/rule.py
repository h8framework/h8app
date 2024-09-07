from abc import abstractmethod
from typing import Any

from h8core import RuleMetaclass


class RuleBase(metaclass=RuleMetaclass):
    @abstractmethod
    def is_satisfied_by(self, input: Any) -> None: ...
