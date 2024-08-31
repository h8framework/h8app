class ModuleMetaclass(type):
    def __init__(cls, name, bases, clsdict) -> None:
        if bases and len(bases) > 1:
            raise TypeError(
                f"You cannot declare multiple inheritance of a module class. Please check implementation of {name}"
            )

        if bases:
            base: type = bases[0]
            for method_name, _ in vars(base).items():
                pass
                # TODO: Verify propeties here

        super(ModuleMetaclass, cls).__init__(name, bases, clsdict)
