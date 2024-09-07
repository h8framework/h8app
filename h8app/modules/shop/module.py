from h8 import AdapterMapping, AdaptersSetup, ComponentsSetup, MiddlewaresSetup, ModuleBase
from h8fastapi import H8FastApiMiddleware
from h8sqla import H8SqlaMiddleware

from .app import builtins, entities, lifespan, listeners, services, specs, tasks, use_cases
from .app.entities import PurchaseOrder
from .infra.repositories import PurchaseOrderMongoRepositoryAdapter


class ShopModule(ModuleBase):
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

    adapters = AdaptersSetup(
        AdapterMapping(entity=PurchaseOrder, impl=PurchaseOrderMongoRepositoryAdapter()),
    )

    middlewares = MiddlewaresSetup(
        H8SqlaMiddleware(),
        H8FastApiMiddleware(),
    )
