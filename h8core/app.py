__all__ = [
    "AppBaseMetaclass",
]


class AppBaseMetaclass(type):
    def __init__(cls, name, bases, clsdict) -> None:
        if bases and len(bases) > 1:
            raise TypeError(
                f"You cannot declare multiple inheritance of a module class. Please check implementation of {name}"
            )

        if bases:
            base: type = bases[0]
            for method_name, _ in vars(base).items():
                pass
                # TODO: Design the implementation

        super(AppBaseMetaclass, cls).__init__(name, bases, clsdict)
