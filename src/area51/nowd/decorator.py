import inspect

from .descriptors import NowdDescriptor
from .arguments import ArgsNowdDescriptor

def nowd(fget, *args, **kwargs):
    signature = inspect.signature(fget)

    base = ArgsNowdDescriptor if len(signature.parameters) > 1 else NowdDescriptor
    cls = type(fget.__code__.co_name + 'Descriptor', (base, ), {})

    return cls(fget, *args, **kwargs)