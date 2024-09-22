from .bases import MiddlewaresSetupBase

__all__ = [
    "ComponentMetaclass",
]


class ComponentMetaclass(type):
    def __init__(cls, name, bases, clsdict) -> None:
        if bases and len(bases) > 1:
            raise TypeError(
                f"You cannot declare multiple inheritance of a component class. Please check implementation of {name}"
            )

        if bases:
            base: type = bases[0]

            validation_list = [
                ("middlewares", MiddlewaresSetupBase),
            ]

            for attr_name, clsbase in validation_list:
                if not hasattr(cls, attr_name):
                    raise AttributeError(
                        f"Property '{attr_name}' must be defined in the class '{name}' derived from '{base.__name__}'"
                    )

                if not isinstance(getattr(cls, attr_name), clsbase):
                    raise AttributeError(f"Property '{attr_name}' must be an instance of {clsbase}.")

        super(ComponentMetaclass, cls).__init__(name, bases, clsdict)
