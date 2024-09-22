from h8core import AppBaseMetaclass, AppSetupBase


class AppBase(metaclass=AppBaseMetaclass):
    pass


class AppSetup(AppSetupBase):
    def __init__(self, app: AppBase) -> None:
        raise NotImplementedError("Not Implemented")
