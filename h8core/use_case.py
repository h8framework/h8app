from .check_subclasses_from_abract_class import check_subclasses_from_abstract_class

__all__ = [
    "UseCaseMetaclass",
]


class UseCaseMetaclass(type):
    def __init__(cls, name, bases, clsdict) -> None:
        check_subclasses_from_abstract_class(cls, name, bases)
        super(UseCaseMetaclass, cls).__init__(name, bases, clsdict)
