from h8 import H8AppBase, Modules

from . import modules


class H8AppBase(H8AppBase):
    modules = Modules(modules)
