import asyncio
import typing
import inspect
import functools

from starlette.concurrency import run_in_threadpool


def complicating(func: typing.Callable) -> typing.Callable[..., typing.Awaitable]:
    """
    always return a awaitable callable object
    """
    if asyncio.iscoroutinefunction(func):
        return func

    _func = func
    while hasattr(_func, "__wrapped__"):
        _func = _func.__wrapped__  # type: ignore

    if asyncio.iscoroutinefunction(_func):
        return func

    if not (inspect.isfunction(_func) or inspect.ismethod(_func)):
        if inspect.isclass(_func):
            # class that has `__await__` method
            if hasattr(_func, "__await__"):
                return func
        else:
            # callable object
            if inspect.iscoroutinefunction(_func.__call__):  # type: ignore
                return func

    @functools.wraps(func)
    async def wrapper(*args, **kwargs) -> typing.Any:
        return await run_in_threadpool(func, *args, **kwargs)

    return wrapper


def keepasync(*args: str) -> typing.Type[type]:
    """
    Ensure that the specified method must be an asynchronous function

    example:

        class T(metaclass=keepasync("a", "b")):
            def a(self):
                pass

            async def b(self):
                pass
    """

    class AlwaysAsyncMeta(type):
        def __new__(cls, clsname, bases, clsdict):
            for name in args:
                if name not in clsdict:
                    continue
                clsdict[name] = complicating(clsdict[name])
            return super().__new__(cls, clsname, bases, clsdict)

    return AlwaysAsyncMeta
