__version__ = "0.0.1"

from h8 import H8AppBase

from . import modules


class H8App(H8AppBase):
    modules = [modules]
