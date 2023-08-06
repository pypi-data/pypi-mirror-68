import functools
import inspect
import typing

__version__ = "0.1.0"
__version_info__ = tuple(__version__.split("."))


def convert(**converter: typing.Callable):
    def wrapper(func):
        spec = inspect.getfullargspec(func)

        def _gen_args(args):
            for arg, value in zip(spec.args, args):
                yield converter[arg](value) if arg in converter else value

            min_args = min(len(spec.args), len(args))
            if spec.varargs in converter:
                yield from map(converter[spec.varargs], args[min_args:])
            else:
                yield from args[min_args:]

        def _gen_kwargs(kwargs):
            converted_kwargs = {}
            varkw_conv = converter.get(spec.varkw, lambda value: value)
            for name in kwargs:
                if name in converter and name != spec.varargs:
                    converted_kwargs[name] = converter[name](kwargs[name])
                else:
                    converted_kwargs[name] = varkw_conv(kwargs[name])

            return converted_kwargs

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            converted_args = _gen_args(args)
            converted_kwargs = _gen_kwargs(kwargs)
            return func(*converted_args, **converted_kwargs)

        return wrapped

    return wrapper
