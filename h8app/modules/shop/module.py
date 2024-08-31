from h8 import AdapterMapping, Adapters, Components, Middlewares, ModuleBase
from h8fastapi import H8FastApiMiddleware
from h8sqla import H8SqlaMiddleware

from .app import builtins, entities, lifespan, listeners, services, specs, tasks, use_cases
from .app.entities import PurchaseOrder
from .infra.repositories import PurchaseOrderMongoRepositoryAdapter


class ShopModule(ModuleBase):
    components = Components(
        lifespan,
        use_cases,
        builtins,
        entities,
        listeners,
        services,
        tasks,
        specs,
    )

    adapters = Adapters(
        AdapterMapping(entity=PurchaseOrder, impl=PurchaseOrderMongoRepositoryAdapter()),
    )

    middlewares = Middlewares(
        H8SqlaMiddleware(),
        H8FastApiMiddleware(),
    )
