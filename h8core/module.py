from .check_metaclass import check_module_properties


class ModuleMetaclass(type):
    def __init__(cls, name, bases, clsdict) -> None:
        # TODO: Verify propeties here
        check_module_properties(cls, name, bases)

        super(ModuleMetaclass, cls).__init__(name, bases, clsdict)
