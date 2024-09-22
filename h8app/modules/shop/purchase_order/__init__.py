from h8 import ComponentBase, MiddlewaresSetup
from h8fastapi import H8FastApiMiddleware
from h8sqla import H8SqlaMiddleware


class PurchaseOrderComponent(ComponentBase):
    middlewares = MiddlewaresSetup(
        H8FastApiMiddleware(),
        H8SqlaMiddleware(),
    )
