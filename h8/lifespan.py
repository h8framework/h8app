from abc import abstractmethod

from h8core import LifespanBaseMetaclass


class LifespanBase(metaclass=LifespanBaseMetaclass):
    @abstractmethod
    def startup(self) -> None: ...

    @abstractmethod
    def shutdown(self) -> None: ...
