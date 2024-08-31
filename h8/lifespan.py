from abc import abstractmethod

from h8core import LifespanMetaclass


class LifespanBase(metaclass=LifespanMetaclass):
    @abstractmethod
    def startup(self) -> None: ...

    @abstractmethod
    def shutdown(self) -> None: ...
