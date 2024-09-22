from typing import Any


class AdapterChoiceBase:
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        raise NotImplementedError()
