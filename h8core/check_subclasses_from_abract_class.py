def check_subclasses_from_abstract_class(cls, name, bases, allow_multi_inheritance_num: int = 1):
    if bases and len(bases) > allow_multi_inheritance_num:
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
