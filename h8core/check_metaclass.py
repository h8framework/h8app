def check_metaclass(cls, name, bases):
    if bases and len(bases) > 1:
        raise TypeError(
            f"You cannot declare multiple inheritance of a class that defines abstract methods. Please check implementation of {name}"
        )

    if bases:
        base: type = bases[0]
        for method_name, _ in vars(base).items():
            subclass_method = getattr(cls, method_name)
            if getattr(subclass_method, "__isabstractmethod__", False):
                raise TypeError(
                    f"Can't create new class {name} with no abstract classmethod {method_name} redefined in the metaclass"
                )




def check_module_properties(cls, name, bases):
    if bases and len(bases) > 1:
        raise TypeError(
            f"You cannot declare multiple inheritance of a module class. Please check implementation of {name}"
        )

    if bases:
        base: type = bases[0]
        for attr_name, attr_value in vars(base).items():
            if isinstance(attr_value, property):
                if not hasattr(cls, attr_name):
                    raise AttributeError(
                        f"Property '{attr_name}' must be defined in the class '{name}' derived from '{base.__name__}'"
                    )
                