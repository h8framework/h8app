from .check_subclasses_from_abract_class import check_subclasses_from_abstract_class

__all__ = [
    "LifespanBaseMetaclass",
]


class LifespanBaseMetaclass(type):
    def __init__(cls, name, bases, clsdict) -> None:
        check_subclasses_from_abstract_class(cls, name, bases)
        super(LifespanBaseMetaclass, cls).__init__(name, bases, clsdict)
