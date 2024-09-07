from .check_subclasses_from_abract_class import check_subclasses_from_abstract_class

__all__ = [
    "RuleMetaclass",
]


class RuleMetaclass(type):
    def __init__(cls, name, bases, clsdict) -> None:
        check_subclasses_from_abstract_class(cls, name, bases)
        super(RuleMetaclass, cls).__init__(name, bases, clsdict)
