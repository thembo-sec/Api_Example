from typing import Any


class NewClass:

    def __init__(self) -> None:
        return

    # def __getattribute__(self, name: str) -> Any:
    #     print(f"Calling __getattribute__ on {name}")
    #     raise AttributeError

    # def __getattr__(self, name: str):
    #     print(f"Calling __getattr__ on {name}")

    def __call__(self, *args, **kwags):
        print(f"Calling __call__ on {self} with args: {args}; and kwargs: {kwags}")


new = NewClass()

new.attr
new()
