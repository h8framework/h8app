from h8 import ComponentBase, MiddlewaresSetup
from h8app.settings.database import DatabaseSettings
from h8fastapi import H8FastApiMiddleware
from h8sqla import H8SqlaMiddleware

_DATABASE_SETTINGS = DatabaseSettings()


class ProductComponent(ComponentBase):
    middlewares = MiddlewaresSetup(
        H8FastApiMiddleware(),
        H8SqlaMiddleware(
            host=_DATABASE_SETTINGS.DATABASE_HOST,
            port=_DATABASE_SETTINGS.DATABASE_PORT,
            username=_DATABASE_SETTINGS.DATABASE_USERNAME,
            password=_DATABASE_SETTINGS.DATABASE_PASSWORD,
            database=_DATABASE_SETTINGS.DATABASE_NAME,
            pool_size=_DATABASE_SETTINGS.DATABASE_POOL_SIZE,
        ),
    )
