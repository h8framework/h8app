from h8core import MiddlewareBaseMetaclass, MiddlewaresSetupBase


class MiddlewareBase(metaclass=MiddlewareBaseMetaclass):
    pass


class MiddlewaresSetup(MiddlewaresSetupBase):
    def __init__(self, *args: MiddlewareBase) -> None:
        pass
