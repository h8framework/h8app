from h8 import App, Modules

from . import modules


class H8App(App):
    modules = Modules(modules)
