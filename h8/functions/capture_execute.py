def capture_execute(self, name):
    attr = object.__getattribute__(self, name)
    if name != "execute":
        return attr

    if not hasattr(attr, "__call__"):
        raise RuntimeError("Bad implementation of 'execute' method. The method should be callable.")

    def wrapper(*args, **kwargs):
        try:
            return attr(*args, **kwargs)
        except Exception as error:
            self.on_error(error)

    return wrapper
