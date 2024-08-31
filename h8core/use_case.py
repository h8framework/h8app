from .check_metaclass import check_metaclass


class UseCaseMetaclass(type):
    def __init__(cls, name, bases, clsdict) -> None:
        check_metaclass(cls, name, bases)
        super(UseCaseMetaclass, cls).__init__(name, bases, clsdict)
