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
                