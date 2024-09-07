from h8 import ComponentsSetup, MiddlewaresSetup, ModuleBase
from h8fastapi import H8FastApiMiddleware
from h8sqla import H8SqlaMiddleware

from .app import builtins, entities, lifespan, listeners, services, specs, tasks, use_cases


class StockModule(ModuleBase):
    components = ComponentsSetup(
        lifespan,
        use_cases,
        builtins,
        entities,
        listeners,
        services,
        tasks,
        specs,
    )

    middlewares = MiddlewaresSetup(
        H8SqlaMiddleware(),
        H8FastApiMiddleware(),
    )
