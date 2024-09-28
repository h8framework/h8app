from h8 import MiddlewareBase


class H8SqlaMiddleware(MiddlewareBase):
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
        pool_size: int,
    ) -> None:
        super().__init__()
